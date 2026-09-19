"""
Deśa-Kāla Sankalpa generator for traditional Vedic pujas and rituals.
Automatically generates location-appropriate geography (Jambudvipe / America Khande...)
and exact astronomical time coordinates in all Indian languages.
"""

from services.localization_service import transliterate_text

COUNTRY_DESA_MAP = {
    "India": {
        "dveepa": "जम्बूद्वीपे",
        "varsha": "भारतवर्षे",
        "khanda": "भरतखण्डे",
        "direction": "मेरोर्दक्षिणदिग्भागे",
        "river_default": "गोदावर्याः / कृष्णायाः / गङ्गायाः शुभतीरे"
    },
    "USA": {
        "dveepa": "क्रौञ्चद्वीपे",
        "varsha": "ऐन्द्रखण्डे",
        "khanda": "उत्तर-अमेरिका-देशे",
        "direction": "मेरोः पश्चिमे",
        "river_default": "मिसिसिपी-नद्याः शुभतीरे"
    },
    "UK": {
        "dveepa": "प्लक्षद्वीपे",
        "varsha": "यूरोप्-खण्डे",
        "khanda": "इङ्ग्लेण्ड्-देशे",
        "direction": "मेरोः पश्चिमे",
        "river_default": "थेम्स्-नद्याः शुभतीरे"
    },
    "Australia": {
        "dveepa": "शाल्मलीद्वीपे",
        "varsha": "ऑस्ट्रेलिया-खण्डे",
        "khanda": "दक्षिण-समुद्र-मध्यभागे",
        "direction": "मेरोर्दक्षिणे",
        "river_default": "शुभतीरे"
    },
    "Canada": {
        "dveepa": "क्रौञ्चद्वीपे",
        "varsha": "ऐन्द्रखण्डे",
        "khanda": "कैनडा-देशे",
        "direction": "मेरोः पश्चिमे",
        "river_default": "शुभतीरे"
    }
}


from typing import Optional

def generate_sankalpam(
    city_name: str,
    country: str,
    samvatsara_sa: str,
    ayana_sa: str,
    ritu_sa: str,
    masa_sa: str,
    paksha_sa: str,
    tithi_sa: str,
    nakshatra_sa: str,
    weekday_sa: str,
    target_lang: str = "telugu",
    kula_devata: Optional[str] = None,
    gotra: Optional[str] = None,
    sharma_name: Optional[str] = None
) -> dict:
    """Generate complete classical Sankalpam text in Sanskrit and translated to target language."""
    
    desa_info = COUNTRY_DESA_MAP.get(country, COUNTRY_DESA_MAP.get("India"))
    
    # Personalization line
    gotra_part = f"{gotra}सगोत्रस्य" if gotra else "अस्मत्-गोत्रस्य"
    name_part = f"{sharma_name}-शर्मणः" if sharma_name else ""
    devata_part = kula_devata if kula_devata else "श्रीपरमेश्वर"
    
    personal_sa = f"मम उपात्त-दुरितक्षयद्वारा {gotra_part} {name_part} {devata_part}-प्रीत्यर्थं शुभकार्यं करिष्ये ॥".strip()

    sankalpa_lines_sa = [
        "श्री गुरुभ्यो नमः । हरिः ॐ ॥",
        "श्रीमद्-भगवतो महापुरुषस्य विष्णोराज्ञया प्रवर्तमानस्य, अद्य ब्रह्मणः द्वितीय-परार्धे, श्वेतवराह-कल्पे, वैवस्वतमन्वन्तरे, अष्टाविंशतितमे कलियुगे, प्रथमपादे,",
        f"{desa_info['dveepa']}, {desa_info['varsha']}, {desa_info['khanda']}, {desa_info['direction']}, {city_name} नगरे / क्षेत्रे, {desa_info['river_default']},",
        f"अस्मिन् वर्तमाने व्यावहारिक चान्द्रमानेन {samvatsara_sa}-नाम-संवत्सरे, {ayana_sa}, {ritu_sa}, {masa_sa}-मासे, {paksha_sa}-पक्षे, {tithi_sa}-तिथौ, {weekday_sa}-वासरे, {nakshatra_sa}-युक्त-नक्षत्रे, शुभयोगे, शुभकरणे, एवं गुण-विशेषण-विशिष्टायां शुभपुण्यतिथौ,",
        personal_sa
    ]
    
    full_text_sa = "\n\n".join(sankalpa_lines_sa)
    full_text_user = transliterate_text(full_text_sa, target_lang)
    
    return {
        "sankalpam_text": full_text_user,
        "full_sankalpam_text": full_text_user,
        "sankalpam_sanskrit_devanagari": full_text_sa,
        "location_context": {
            "city": city_name,
            "country": country,
            "dveepa": transliterate_text(desa_info['dveepa'], target_lang),
            "khanda": transliterate_text(desa_info['khanda'], target_lang)
        }
    }