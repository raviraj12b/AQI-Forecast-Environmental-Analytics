"""
Health recommendations service for the AQI Forecast & Environmental
Analytics Platform (UI-HEALTH-001).

Content follows the standard structure of published AQI health-category
guidance (description, health risk, outdoor recommendation, safety
advice) for each of the 6 categories already defined in
`config.constants.AQI_CATEGORIES`. This is general public-health guidance,
not individualized medical advice -- the dashboard should present it as
such (see `disclaimer` below).
"""

from typing import Optional

from config.constants import AQI_CATEGORIES
from src.utils.logger import get_logger

logger = get_logger(__name__)

disclaimer = (
    "This is general guidance based on standard AQI health-category "
    "thresholds, not individualized medical advice. Sensitive individuals "
    "(children, elderly, those with respiratory or cardiovascular "
    "conditions) should consult a healthcare provider for personal guidance."
)

_HEALTH_GUIDANCE = {
    "Good": {
        "description": "Air quality is satisfactory, and air pollution poses little or no risk.",
        "health_risk": "Minimal risk to the general population.",
        "outdoor_recommendation": "Outdoor activities are safe for everyone.",
        "safety_advice": "No precautions needed.",
    },
    "Moderate": {
        "description": "Air quality is acceptable. However, there may be a risk for some people, particularly those unusually sensitive to air pollution.",
        "health_risk": "Unusually sensitive individuals may experience minor respiratory symptoms.",
        "outdoor_recommendation": "Outdoor activities are generally safe.",
        "safety_advice": "Unusually sensitive individuals should consider limiting prolonged outdoor exertion.",
    },
    "Unhealthy for Sensitive Groups": {
        "description": "Members of sensitive groups may experience health effects; the general public is less likely to be affected.",
        "health_risk": "Increased risk for children, elderly, and those with asthma, lung, or heart disease.",
        "outdoor_recommendation": "Sensitive groups should reduce prolonged or heavy outdoor exertion.",
        "safety_advice": "Sensitive individuals should watch for symptoms such as coughing or shortness of breath.",
    },
    "Unhealthy": {
        "description": "Everyone may begin to experience health effects; sensitive groups may experience more serious effects.",
        "health_risk": "Increased likelihood of respiratory symptoms in the general population; more serious effects for sensitive groups.",
        "outdoor_recommendation": "Everyone should reduce prolonged or heavy outdoor exertion; sensitive groups should avoid it.",
        "safety_advice": "Consider wearing a pollution mask outdoors; keep windows closed; use an air purifier indoors if available.",
    },
    "Very Unhealthy": {
        "description": "Health alert: the risk of health effects is increased for everyone.",
        "health_risk": "Significant increase in respiratory and cardiovascular symptoms across the general population.",
        "outdoor_recommendation": "Everyone should avoid prolonged or heavy outdoor exertion; sensitive groups should avoid outdoor activity entirely.",
        "safety_advice": "Minimize time outdoors; use a properly rated pollution mask (e.g. N95) if going outside is unavoidable; keep indoor air filtered.",
    },
    "Hazardous": {
        "description": "Health warning of emergency conditions: everyone is more likely to be affected.",
        "health_risk": "Serious risk of respiratory and cardiovascular effects for the entire population.",
        "outdoor_recommendation": "Everyone should avoid all outdoor physical activity. Remain indoors and keep activity levels low.",
        "safety_advice": "Stay indoors with windows/doors closed; run air purifiers; seek medical attention if experiencing difficulty breathing, chest pain, or dizziness.",
    },
}


def get_health_recommendation(category: str) -> Optional[dict]:
    """
    Return the health guidance dict for an AQI category label (one of the
    labels in `config.constants.AQI_CATEGORIES`).

    Returns
    -------
    dict or None
        {"category", "aqi_range", "description", "health_risk",
        "outdoor_recommendation", "safety_advice"}, or None if `category`
        isn't a recognized label.
    """
    if category not in _HEALTH_GUIDANCE:
        logger.warning("get_health_recommendation: unrecognized category '%s'.", category)
        return None

    breakpoint_entry = next(c for c in AQI_CATEGORIES if c["label"] == category)
    guidance = dict(_HEALTH_GUIDANCE[category])
    guidance["category"] = category
    guidance["aqi_range"] = f"{breakpoint_entry['min']}\u2013{breakpoint_entry['max']}"
    return guidance


def get_recommendation_for_aqi(aqi: float) -> Optional[dict]:
    """Convenience wrapper: look up guidance directly from a numeric AQI value."""
    for cat in AQI_CATEGORIES:
        if cat["min"] <= aqi <= cat["max"]:
            return get_health_recommendation(cat["label"])
    return None
