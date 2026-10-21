"""Maharashtra-focused fertilizer guidance shared by the guide and search API."""

FERTILIZERS = {
    "farmyard-manure": {
        "name": "Farmyard Manure (FYM)", "type": "Organic", "main_nutrients": "Low, broad N-P-K plus organic carbon and micronutrients",
        "benefits": "Improves soil structure, microbial activity, water holding and long-term nutrient availability.",
        "suitable_crops": "All field crops, vegetables, fruit orchards, sugarcane and flowers",
        "crop_terms": "rice wheat maize jowar bajra cotton soybean sugarcane chickpea groundnut sunflower onion tomato potato brinjal eggplant chilli pepper okra bhindi cabbage cauliflower leafy vegetables banana grapes pomegranate mango orange",
        "suitable_soils": "All soils; especially low-organic-carbon black, red, laterite, sandy and degraded soils",
        "application": "Use only well-decomposed FYM. Broadcast and incorporate before sowing or place in pits/basins for orchards; combine with a soil-test-based nutrient plan.",
        "stage": "Land preparation, normally 2-4 weeks before sowing or transplanting; orchard basins before the main growth flush.",
        "precautions": "Do not use fresh or partly decomposed manure near seed or roots. Avoid material contaminated with plastics, weed seed, salts or pesticide waste."
    },
    "vermicompost": {
        "name": "Vermicompost", "type": "Organic", "main_nutrients": "Organic carbon, modest N-P-K and micronutrients",
        "benefits": "Supports root growth, soil aggregation and beneficial microbial activity with slowly available nutrients.",
        "suitable_crops": "Vegetables, nurseries, flowers, onion, fruit crops and kitchen gardens",
        "crop_terms": "vegetable vegetables tomato potato brinjal eggplant chilli pepper okra bhindi onion cabbage cauliflower leafy nursery flowers banana grapes pomegranate mango citrus orange",
        "suitable_soils": "Red, laterite, sandy, loamy and low-organic-matter black soils",
        "application": "Mix into beds, planting pits or root-zone soil; use as a supplement rather than the sole nutrient source for high-yield crops.",
        "stage": "Before planting and as a light root-zone application during early growth.",
        "precautions": "Buy mature, cool, earthy-smelling compost from a reliable source. Keep shaded and moist; do not mix directly with concentrated chemicals."
    },
    "neem-cake": {
        "name": "Neem Cake", "type": "Organic", "main_nutrients": "Organic nitrogen with small amounts of phosphorus, potassium and neem compounds",
        "benefits": "Adds organic matter and nutrients and may help suppress some soil pests and reduce nitrogen loss.",
        "suitable_crops": "Vegetables, sugarcane, cotton, rice, fruit crops and flowers",
        "crop_terms": "vegetable vegetables tomato potato brinjal eggplant chilli pepper okra bhindi onion cabbage cauliflower sugarcane cotton rice banana grapes pomegranate mango orange flowers",
        "suitable_soils": "Black, red, laterite, loamy and sandy soils",
        "application": "Incorporate into moist soil before planting or apply around the root zone and cover lightly.",
        "stage": "Land preparation or planting; repeat only according to crop guidance.",
        "precautions": "Use genuine, properly processed cake. Keep away from livestock feed and do not assume it replaces crop-specific pest management."
    },
    "urea": {
        "name": "Urea", "type": "Chemical", "main_nutrients": "46% nitrogen (46-0-0)",
        "benefits": "Quickly corrects nitrogen demand and supports vegetative growth, leaf area and yield when properly timed.",
        "suitable_crops": "Rice, wheat, maize, jowar, bajra, sugarcane, cotton, onion and most vegetables when nitrogen is required",
        "crop_terms": "rice wheat maize corn jowar sorghum bajra millet sugarcane cotton onion vegetable vegetables tomato potato brinjal eggplant chilli pepper okra bhindi cabbage cauliflower leafy",
        "suitable_soils": "Most tested agricultural soils; split doses are especially important in sandy and high-rainfall soils",
        "application": "Apply soil-test-based nitrogen in splits, band or side-dress into moist soil, and irrigate lightly when rain is not expected. Neem-coated urea is preferred where available.",
        "stage": "Crop-specific splits, commonly early vegetative growth, tillering or rapid canopy development; avoid late excess application.",
        "precautions": "Never place against seed, stem or wet leaves. Do not apply before heavy rain or on flooded/drained-away water. Excess nitrogen increases lodging, pests and poor produce quality."
    },
    "dap": {
        "name": "DAP (Diammonium Phosphate)", "type": "Chemical", "main_nutrients": "18% nitrogen and 46% phosphate (18-46-0)",
        "benefits": "Supplies starter nitrogen and concentrated phosphorus for early rooting and establishment.",
        "suitable_crops": "Cotton, cereals, pulses, soybean, groundnut, sugarcane and vegetables where soil phosphorus is deficient",
        "crop_terms": "cotton rice wheat maize corn jowar bajra chickpea gram pulse pulses soybean groundnut sugarcane vegetable vegetables tomato potato brinjal chilli onion cabbage cauliflower",
        "suitable_soils": "Low-phosphorus black, red, laterite and loamy soils, subject to soil-test recommendation",
        "application": "Band as a basal fertilizer below and to the side of seed/root placement; account for its nitrogen in the full nutrient plan.",
        "stage": "At sowing or transplanting; phosphorus is most valuable during establishment.",
        "precautions": "Prevent direct seed/root contact. Do not use routinely when phosphorus is already high, and do not mix/store with incompatible materials such as lime."
    },
    "ssp": {
        "name": "Single Super Phosphate (SSP)", "type": "Chemical", "main_nutrients": "About 16% phosphate plus sulphur and calcium",
        "benefits": "Supports roots, nodulation and oil/protein formation while supplying useful sulphur.",
        "suitable_crops": "Soybean, groundnut, chickpea, sunflower, onion, pulses and oilseeds",
        "crop_terms": "soybean groundnut peanut chickpea gram pulse pulses sunflower oilseed oilseeds onion garlic",
        "suitable_soils": "Sulphur- or phosphorus-deficient black, red and loamy soils",
        "application": "Apply basally and incorporate or band near, but not touching, seed; use the soil test to choose between SSP and other phosphorus sources.",
        "stage": "Before or at sowing/transplanting.",
        "precautions": "Avoid unnecessary phosphorus buildup. Store dry and use certified material; placement and quantity must follow the crop recommendation."
    },
    "mop": {
        "name": "MOP (Muriate of Potash)", "type": "Chemical", "main_nutrients": "60% potash (0-0-60), supplied as potassium chloride",
        "benefits": "Improves water regulation, stem strength, stress tolerance, grain filling and produce quality where potassium is deficient.",
        "suitable_crops": "Rice, wheat, maize, cotton, sugarcane and many vegetables; use alternatives for chloride-sensitive crops",
        "crop_terms": "rice wheat maize corn cotton sugarcane vegetable vegetables tomato potato brinjal eggplant chilli pepper okra bhindi cabbage cauliflower onion",
        "suitable_soils": "Potassium-deficient light, red, laterite and loamy soils; only after testing in potassium-rich black soils",
        "application": "Broadcast/incorporate or band as basal fertilizer; split on light soils or long-duration crops.",
        "stage": "Basal and, where recommended, before flowering, fruiting or bulking.",
        "precautions": "Chloride can injure sensitive crops and salinity-prone soils. Keep away from seed and never assume all black soils need potash."
    },
    "sop": {
        "name": "SOP (Sulphate of Potash)", "type": "Chemical", "main_nutrients": "About 50% potash plus 17-18% sulphur; low chloride",
        "benefits": "Supports fruit size, colour, sweetness and quality while supplying sulphur without a high chloride load.",
        "suitable_crops": "Grapes, pomegranate, banana, potato, onion, tomato, chilli and other quality-sensitive horticultural crops",
        "crop_terms": "grapes grape pomegranate banana potato onion tomato chilli pepper vegetable vegetables fruit fruits orchard horticulture",
        "suitable_soils": "Soils needing potassium where salinity or chloride sensitivity makes MOP unsuitable",
        "application": "Apply to soil or through fertigation only in fully soluble grades and according to water, soil and tissue tests.",
        "stage": "Fruit development, bulking and quality-building stages as part of a balanced programme.",
        "precautions": "More expensive than MOP and not automatically better. Avoid excessive potassium, which can disturb magnesium and calcium uptake."
    },
    "npk-complex": {
        "name": "NPK Complex Fertilizer", "type": "Chemical", "main_nutrients": "Balanced grades such as 10-26-26, 12-32-16 or 15-15-15",
        "benefits": "Provides uniform granules containing multiple primary nutrients for convenient basal nutrition.",
        "suitable_crops": "Cereals, cotton, sugarcane, vegetables, flowers and orchards when the chosen grade matches the soil test",
        "crop_terms": "rice wheat maize jowar bajra cotton sugarcane vegetable vegetables tomato potato brinjal chilli okra onion cabbage cauliflower flowers banana grapes pomegranate mango orange orchard",
        "suitable_soils": "Black, red, laterite, loamy and alluvial soils according to nutrient status",
        "application": "Select the grade from soil-test needs, apply basally in bands or around the active root zone, and supplement later nutrients separately if required.",
        "stage": "Sowing/transplanting or early crop growth; orchard timing follows crop stage and local recommendation.",
        "precautions": "A fixed grade rarely matches every field. Calculate each nutrient contribution to prevent excess phosphorus or potassium."
    },
    "calcium-ammonium-nitrate": {
        "name": "Calcium Ammonium Nitrate (CAN)", "type": "Chemical", "main_nutrients": "About 25-26% nitrogen plus calcium",
        "benefits": "Supplies readily available nitrogen with calcium and is less acidifying than some nitrogen sources.",
        "suitable_crops": "Vegetables, fruit crops, wheat, maize and flowers where nitrogen and calcium are needed",
        "crop_terms": "vegetable vegetables tomato potato brinjal chilli pepper okra cabbage cauliflower fruit fruits banana grapes pomegranate citrus orange wheat maize corn flowers",
        "suitable_soils": "Acidic to neutral, well-drained soils; use cautiously in saline conditions",
        "application": "Side-dress into moist soil or fertigate only with a suitable soluble product and compatible stock-tank practice.",
        "stage": "Active vegetative growth and crop-specific fruit development splits.",
        "precautions": "Keep dry and away from heat, fuels and incompatible chemicals. Do not mix concentrated calcium solutions with phosphates or sulphates."
    },
    "zinc-sulphate": {
        "name": "Zinc Sulphate", "type": "Chemical / Micronutrient", "main_nutrients": "Zinc plus sulphur (concentration depends on hydrated form)",
        "benefits": "Corrects confirmed zinc deficiency, improving enzyme activity, growth and grain formation.",
        "suitable_crops": "Rice, wheat, maize, sugarcane, cotton, onion and vegetables on zinc-deficient fields",
        "crop_terms": "rice wheat maize corn sugarcane cotton onion vegetable vegetables tomato potato brinjal chilli okra cabbage cauliflower",
        "suitable_soils": "High-pH, calcareous, intensively cropped or zinc-deficient soils confirmed by testing",
        "application": "Use soil application or a correctly diluted foliar spray exactly as recommended by the soil-test laboratory or agriculture officer.",
        "stage": "Basal correction or early growth when deficiency symptoms/testing indicate need.",
        "precautions": "Micronutrient overuse can be toxic. Confirm deficiency and product concentration; never copy a dose between 21% and 33% zinc products."
    },
    "gypsum": {
        "name": "Agricultural Gypsum", "type": "Mineral soil amendment", "main_nutrients": "Calcium and sulphur",
        "benefits": "Supplies calcium/sulphur, supports groundnut pod filling and can help reclaim sodic soil under a tested programme.",
        "suitable_crops": "Groundnut, onion, oilseeds, pulses and crops on diagnosed sodic soils",
        "crop_terms": "groundnut peanut onion garlic oilseed oilseeds chickpea gram pulse pulses",
        "suitable_soils": "Sulphur/calcium-deficient soils and laboratory-diagnosed sodic soils; not a universal pH treatment",
        "application": "For crops, incorporate the recommended grade/quantity; for groundnut, apply around pegging as locally advised. Sodic reclamation requires lab-calculated gypsum requirement and drainage.",
        "stage": "Basal or groundnut flowering/pegging; reclamation before cropping.",
        "precautions": "Gypsum does not replace lime for acidic soil. Use agricultural-grade material and verify sodicity before reclamation use."
    },
    "rhizobium": {
        "name": "Rhizobium Biofertilizer", "type": "Biofertilizer", "main_nutrients": "Living crop-specific nitrogen-fixing bacteria",
        "benefits": "Improves nodulation and biological nitrogen fixation in compatible legumes, reducing unnecessary nitrogen input.",
        "suitable_crops": "Soybean, chickpea, groundnut, pigeon pea, green gram, black gram and other matched legumes",
        "crop_terms": "soybean chickpea gram groundnut peanut pigeon pea tur arhar green gram mung moong black gram urad pulse pulses legume legumes",
        "suitable_soils": "Most well-drained soils with suitable pH and moisture; performance falls in extreme acidity, salinity or waterlogging",
        "application": "Coat seed with the crop-specific strain using the label method, shade-dry briefly and sow promptly into moist soil.",
        "stage": "Immediately before sowing.",
        "precautions": "Strains are crop-specific. Check expiry and certification, protect from sun/heat, and separate from incompatible seed-treatment chemicals as the label directs."
    },
    "psb": {
        "name": "Phosphate-Solubilizing Bacteria (PSB)", "type": "Biofertilizer", "main_nutrients": "Living microbes that help mobilize some soil phosphorus",
        "benefits": "May improve phosphorus availability and root growth as part of integrated nutrient management.",
        "suitable_crops": "Cereals, pulses, oilseeds, vegetables, sugarcane and fruit crops",
        "crop_terms": "rice wheat maize jowar bajra chickpea soybean groundnut sunflower vegetable vegetables tomato potato brinjal chilli okra onion cabbage cauliflower sugarcane banana grapes pomegranate mango fruit fruits",
        "suitable_soils": "Many agricultural soils, particularly where phosphorus fixation limits availability",
        "application": "Use as certified seed treatment, seedling-root dip or soil application mixed with cool compost, following the product label.",
        "stage": "At sowing or transplanting.",
        "precautions": "It complements rather than automatically replaces recommended phosphorus. Store cool, use before expiry and avoid sun or incompatible chemical contact."
    }
}


def build_fertilizer_catalog(database_fertilizers=None):
    """Return detailed records, retaining a database image when one exists."""
    database_fertilizers = database_fertilizers or {}
    records = []
    for key, details in FERTILIZERS.items():
        legacy = database_fertilizers.get(key.replace("-", "_"), database_fertilizers.get(key, {}))
        records.append({"id": key, "image": legacy.get("image", ""), **details})
    return records


def fertilizer_matches(record, query):
    words = query.lower().strip().replace("-", " ")
    if not words:
        return True
    haystack = " ".join(str(record.get(field, "")) for field in (
        "name", "type", "main_nutrients", "suitable_crops", "crop_terms", "suitable_soils", "benefits"
    )).lower()
    aliases = {"brinjal": "eggplant", "bhindi": "okra", "corn": "maize", "gram": "chickpea", "tur": "pigeon pea"}
    terms = {words, aliases.get(words, "")}
    return any(term and term in haystack for term in terms)
