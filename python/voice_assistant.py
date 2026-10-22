"""Rule-based multilingual agriculture assistant with no paid API dependency."""

import re


LANGUAGES = {"en-IN", "hi-IN", "mr-IN"}

CROP_ALIASES = {
    "rice": ("rice", "paddy", "धान", "चावल", "तांदूळ", "भात"),
    "wheat": ("wheat", "गेहूं", "गहू"),
    "corn": ("corn", "maize", "मक्का", "मकई", "मका"),
    "jowar": ("jowar", "sorghum", "ज्वार", "ज्वारी"),
    "bajra": ("bajra", "pearl millet", "बाजरा", "बाजरी"),
    "cotton": ("cotton", "कपास", "कापूस"),
    "soybean": ("soybean", "सोयाबीन"),
    "sugarcane": ("sugarcane", "गन्ना", "ऊस"),
    "sunflower": ("sunflower", "सूरजमुखी", "सूर्यफूल"),
    "chickpea": ("chickpea", "gram", "चना", "हरभरा"),
    "groundnut": ("groundnut", "peanut", "मूंगफली", "भुईमूग"),
    "onion": ("onion", "प्याज", "कांदा", "कांद"),
}

SOIL_ALIASES = {
    "black soil": ("black soil", "काली मिट्टी", "काळी माती"),
    "clayey soil": ("clay soil", "clayey soil", "चिकनी मिट्टी", "चिकणमाती"),
    "red soil": ("red soil", "लाल मिट्टी", "लाल माती"),
    "sandy soil": ("sandy soil", "रेतीली मिट्टी", "वालुकामय माती"),
    "loamy soil": ("loamy soil", "दोमट मिट्टी", "लोम माती"),
    "silt soil": ("silt soil", "गाद मिट्टी", "गाळाची माती"),
    "laterite soil": ("laterite", "लैटेराइट", "जांभी माती"),
    "alluvial soil": ("alluvial", "जलोढ़", "गाळाची सुपीक माती"),
}


def normalize_language(language):
    return language if language in LANGUAGES else "en-IN"


def _contains(question, words):
    return any(word in question for word in words)


def find_key(question, aliases):
    lowered = question.casefold()
    for key, names in aliases.items():
        if any(name.casefold() in lowered for name in names):
            return key
    return None


def intent(question):
    q = question.casefold()
    if _contains(q, ("price", "rate", "mandi", "market", "भाव", "बाजारभाव", "कीमत", "मंडी")):
        return "market"
    if _contains(q, ("weather", "temperature", "rain", "humidity", "forecast", "मौसम", "बारिश", "तापमान", "हवामान", "पाऊस")):
        return "weather"
    if _contains(q, ("scheme", "subsidy", "government", "योजना", "सब्सिडी", "सरकार", "शासकीय", "अनुदान")):
        return "scheme"
    if _contains(q, ("irrigat", "water", "सिंचाई", "पानी", "सिंचन", "पाणी")):
        return "irrigation"
    if _contains(q, ("soil", "ph", "nutrient", "मिट्टी", "मृदा", "माती", "पोषक")):
        return "soil"
    return "crop"


def _pick(language, en, hi, mr):
    return {"en-IN": en, "hi-IN": hi, "mr-IN": mr}[language]


def answer(question, language, crops, soils):
    """Return a grounded local answer and intent; live intents are completed by app.py."""
    language = normalize_language(language)
    kind = intent(question)
    crop_key = find_key(question, CROP_ALIASES)
    soil_key = find_key(question, SOIL_ALIASES)
    crop = crops.get(crop_key) if crop_key else None
    soil = soils.get(soil_key) if soil_key else None

    if kind == "market":
        return {"intent": kind, "crop_key": crop_key}
    if kind == "weather":
        return {"intent": kind}
    if kind == "scheme":
        text = _pick(language,
            "Government schemes and eligibility can change. Check the official MahaDBT Farmer portal or PM-KISAN portal, and confirm documents with your taluka agriculture office. I will not guess current eligibility or deadlines.",
            "सरकारी योजनाएँ और पात्रता बदल सकती हैं। आधिकारिक MahaDBT Farmer या PM-KISAN पोर्टल देखें और तालुका कृषि कार्यालय से दस्तावेज़ों की पुष्टि करें। मैं मौजूदा पात्रता या अंतिम तिथि का अनुमान नहीं लगाऊँगा।",
            "शासकीय योजना व पात्रता बदलू शकते. अधिकृत MahaDBT Farmer किंवा PM-KISAN पोर्टल तपासा आणि तालुका कृषी कार्यालयाकडून कागदपत्रांची खात्री करा. मी सध्याची पात्रता किंवा अंतिम तारीख अंदाजाने सांगणार नाही.")
        return {"intent": kind, "answer": text, "links": [{"label": "MahaDBT Farmer", "url": "https://mahadbt.maharashtra.gov.in/Farmer"}, {"label": "PM-KISAN", "url": "https://pmkisan.gov.in/"}]}
    if kind == "irrigation" and crop:
        water = crop.get("water", "Use soil moisture and local weather to schedule irrigation.")
        text = _pick(language,
            f"For {crop['name']}: {water} For a field-specific estimate, save your farm in the Smart Irrigation Planner; it uses live weather and optional soil-moisture readings.",
            f"{crop['name']} के लिए: {water} खेत के अनुसार अनुमान पाने के लिए Smart Irrigation Planner में अपना खेत सहेजें; यह लाइव मौसम और वैकल्पिक मिट्टी-नमी रीडिंग का उपयोग करता है।",
            f"{crop['name']} साठी: {water} शेतानुसार अंदाजासाठी Smart Irrigation Planner मध्ये शेताची माहिती जतन करा; तो थेट हवामान आणि ऐच्छिक माती-ओलावा नोंद वापरतो.")
        return {"intent": kind, "answer": text, "link": "/irrigation"}
    if kind == "irrigation":
        text = _pick(language,
            "Irrigate from crop stage, root-zone soil moisture, and forecast—not a fixed calendar alone. Water early morning, avoid waterlogging, and use drip plus mulch where suitable. Save your farm in Smart Irrigation Planner for a weather-based estimate.",
            "सिंचाई केवल तय कैलेंडर से नहीं, बल्कि फसल अवस्था, जड़ क्षेत्र की नमी और मौसम पूर्वानुमान देखकर करें। सुबह पानी दें, जलभराव से बचें और उपयुक्त हो तो ड्रिप व मल्च अपनाएँ। मौसम-आधारित अनुमान के लिए Smart Irrigation Planner में खेत सहेजें।",
            "सिंचन फक्त ठराविक वेळापत्रकानुसार न करता पीक अवस्था, मुळांजवळील ओलावा आणि हवामान अंदाज पाहून करा. सकाळी पाणी द्या, पाणी साचू देऊ नका आणि योग्य असल्यास ठिबक व आच्छादन वापरा. हवामानाधारित अंदाजासाठी Smart Irrigation Planner मध्ये शेत जतन करा.")
        return {"intent": kind, "answer": text, "link": "/irrigation"}
    if kind == "soil" and soil:
        text = _pick(language,
            f"{soil['name']}: pH {soil.get('ph', 'varies')}; suitable crops: {soil.get('best_crops', 'see the soil guide')}. {soil.get('recommendations', soil.get('description', ''))}",
            f"{soil['name']}: pH {soil.get('ph', 'अलग-अलग')}; उपयुक्त फसलें: {soil.get('best_crops', 'मृदा मार्गदर्शिका देखें')}। {soil.get('recommendations', soil.get('description', ''))}",
            f"{soil['name']}: pH {soil.get('ph', 'वेगवेगळा')}; योग्य पिके: {soil.get('best_crops', 'माती मार्गदर्शक पहा')}. {soil.get('recommendations', soil.get('description', ''))}")
        return {"intent": kind, "answer": text, "link": f"/soil/{soil_key}"}
    if crop:
        fields = f"Season: {crop.get('season', 'varies')}. Soil: {crop.get('soil', 'see local guidance')}. Cultivation: {crop.get('cultivation', crop.get('description', ''))} Harvest: {crop.get('harvest', 'depends on variety and conditions')}"
        intro = _pick(language, f"Here is the available guidance for {crop['name']}. ", f"{crop['name']} के लिए उपलब्ध मार्गदर्शन: ", f"{crop['name']} साठी उपलब्ध मार्गदर्शन: ")
        return {"intent": "crop", "answer": intro + fields, "link": f"/crop/{crop_key}"}
    if kind == "soil":
        text = _pick(language,
            "Tell me the soil type or crop. A laboratory soil test is the reliable way to know pH and nutrients; do not choose fertilizer from appearance alone.",
            "मिट्टी का प्रकार या फसल बताइए। pH और पोषक तत्व जानने का विश्वसनीय तरीका प्रयोगशाला मृदा परीक्षण है; केवल मिट्टी देखकर उर्वरक न चुनें।",
            "मातीचा प्रकार किंवा पीक सांगा. pH व अन्नद्रव्ये जाणण्यासाठी प्रयोगशाळेतील माती परीक्षण विश्वासार्ह आहे; फक्त माती पाहून खत निवडू नका.")
    else:
        text = _pick(language,
            "I can help with crops, soil, irrigation, saved-farm weather, live Maharashtra mandi prices, and official scheme guidance. Please mention a crop or soil type for a specific answer.",
            "मैं फसल, मिट्टी, सिंचाई, सहेजे गए खेत का मौसम, महाराष्ट्र के लाइव मंडी भाव और आधिकारिक योजना मार्गदर्शन में मदद कर सकता हूँ। विशेष उत्तर के लिए फसल या मिट्टी का नाम बताइए।",
            "मी पिके, माती, सिंचन, जतन केलेल्या शेताचे हवामान, महाराष्ट्रातील थेट बाजारभाव आणि अधिकृत योजना मार्गदर्शन याबाबत मदत करू शकतो. नेमक्या उत्तरासाठी पीक किंवा मातीचा प्रकार सांगा.")
    return {"intent": kind, "answer": text}


def clean_question(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()[:500]
