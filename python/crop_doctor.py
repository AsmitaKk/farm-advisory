import base64
import json
import os
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError


API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"


class CropDoctorError(RuntimeError):
    pass


def _extract_json(text):
    clean = (text or "").strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    start, end = clean.find("{"), clean.rfind("}")
    if start < 0 or end <= start:
        raise CropDoctorError("The AI service returned an unreadable report. Please try another image.")
    try:
        return json.loads(clean[start:end + 1])
    except json.JSONDecodeError as exc:
        raise CropDoctorError("The AI service returned an invalid report. Please try again.") from exc


def _call_gemini(parts, temperature=0.2):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise CropDoctorError("AI scanning is not configured. Add GEMINI_API_KEY to the server .env file.")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    endpoint = f"{API_ROOT}/{model}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"temperature": temperature, "responseMimeType": "application/json"},
    }).encode("utf-8")
    req = urlrequest.Request(endpoint, data=payload, headers={
        "Content-Type": "application/json", "Accept": "application/json",
        "User-Agent": "AgricultureHelper-CropDoctor/1.0",
    }, method="POST")
    try:
        with urlrequest.urlopen(req, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = ""
        try:
            detail = json.loads(exc.read().decode("utf-8")).get("error", {}).get("message", "")
        except Exception:
            pass
        raise CropDoctorError(f"AI service request failed{': ' + detail[:180] if detail else ''}.") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise CropDoctorError("The AI service is temporarily unavailable. Please try again later.") from exc
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise CropDoctorError("The AI service could not analyze this image safely. Try a clearer crop photo.") from exc
    return _extract_json(text)


def analyze_crop(image_bytes, mime_type, context):
    schema = {
        "image_quality": "good|usable|unclear", "image_quality_note": "string",
        "crop_name": "string or Unknown", "crop_confidence": 0,
        "growth_stage": "string or Not identifiable", "overall_status": "healthy|attention|urgent|uncertain",
        "visible_symptoms": ["string"],
        "possible_issues": [{"name": "string", "type": "disease|pest|nutrient|physical|unknown", "confidence": 0, "evidence": "visible evidence", "causes": "possible causes"}],
        "crop_care": ["string"], "fertilizer_guidance": ["string"],
        "irrigation_guidance": ["string"], "preventive_care": ["string"],
        "expert_advice": "string", "next_inspection_days": 3,
        "limitations": ["string"], "summary": "string"
    }
    prompt = f"""You are a cautious agricultural crop-health screening assistant for farmers in India.
Analyze only visible evidence in the attached crop image and the farmer-supplied context below.
This is screening, not a confirmed diagnosis. Never invent a crop, symptom, weather reading, soil result, dosage, pesticide, or confidence.
If the photo is unclear/non-crop/insufficient, set image_quality=unclear, crop_name=Unknown, overall_status=uncertain, explain how to retake it, and keep possible_issues empty.
Use calibrated integer confidence 0-100. Different conditions can look alike; explicitly recommend expert/lab confirmation for urgent or uncertain issues.
Do not prescribe fertilizer quantities from an image. Only give a quantity or schedule if the supplied soil-test and agronomic context genuinely support it; otherwise recommend soil-test-based planning and explain suitable categories/options without dosage.
Do not recommend restricted chemicals or unsafe mixing. Prefer integrated pest management and label/local-authority guidance.
Weather context may be absent; if absent, label irrigation advice as an estimate. Return ONLY one JSON object matching this shape (arrays must remain arrays):
{json.dumps(schema, ensure_ascii=False)}
Farmer context:
{json.dumps(context, ensure_ascii=False, default=str)}"""
    report = _call_gemini([
        {"text": prompt},
        {"inlineData": {"mimeType": mime_type, "data": base64.b64encode(image_bytes).decode("ascii")}},
    ])
    report["crop_confidence"] = max(0, min(100, int(report.get("crop_confidence") or 0)))
    report["next_inspection_days"] = max(1, min(30, int(report.get("next_inspection_days") or 3)))
    for issue in report.get("possible_issues", []):
        issue["confidence"] = max(0, min(100, int(issue.get("confidence") or 0)))
    return report


def answer_question(question, language, report=None):
    prompt = f"""Answer the farmer's crop-care question in simple {language}.
Be concise, practical, and cautious. Do not claim a confirmed diagnosis. Do not invent live weather, soil data, fertilizer dosage, or pesticide dosage. If exact quantities are requested without crop area, growth stage, and a soil test, explain what information is needed. Suggest a local agriculture officer/KVK when risk is urgent or uncertain.
Related scan report (may be empty): {json.dumps(report or {}, ensure_ascii=False)}
Question: {question}
Return JSON exactly as {{"answer":"...","needs_expert":false}}."""
    return _call_gemini([{"text": prompt}], temperature=0.25)
