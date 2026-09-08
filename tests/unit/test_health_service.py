"""Unit tests for src.services.health_service (UI-HEALTH-001)."""

from config.constants import AQI_CATEGORIES
from src.services.health_service import get_health_recommendation, get_recommendation_for_aqi


def test_every_config_category_has_guidance():
    """No category should be defined in config.constants without matching
    health guidance -- this would be a silent dashboard gap otherwise."""
    for cat in AQI_CATEGORIES:
        guidance = get_health_recommendation(cat["label"])
        assert guidance is not None, f"Missing guidance for '{cat['label']}'"


def test_guidance_has_all_required_fields():
    required_fields = {"category", "aqi_range", "description", "health_risk",
                        "outdoor_recommendation", "safety_advice"}
    for cat in AQI_CATEGORIES:
        guidance = get_health_recommendation(cat["label"])
        assert required_fields.issubset(guidance.keys())


def test_guidance_fields_are_nonempty_strings():
    for cat in AQI_CATEGORIES:
        guidance = get_health_recommendation(cat["label"])
        for field in ["description", "health_risk", "outdoor_recommendation", "safety_advice"]:
            assert isinstance(guidance[field], str)
            assert len(guidance[field]) > 0


def test_unrecognized_category_returns_none():
    assert get_health_recommendation("Not A Real Category") is None


def test_aqi_range_matches_config_breakpoints():
    guidance = get_health_recommendation("Good")
    assert guidance["aqi_range"] == "0\u201350"


def test_get_recommendation_for_aqi_looks_up_correct_category():
    assert get_recommendation_for_aqi(25)["category"] == "Good"
    assert get_recommendation_for_aqi(75)["category"] == "Moderate"
    assert get_recommendation_for_aqi(400)["category"] == "Hazardous"


def test_get_recommendation_for_aqi_boundary_values():
    # boundaries are inclusive per config.constants.AQI_CATEGORIES
    assert get_recommendation_for_aqi(50)["category"] == "Good"
    assert get_recommendation_for_aqi(51)["category"] == "Moderate"


def test_get_recommendation_for_aqi_out_of_range_returns_none():
    assert get_recommendation_for_aqi(-10) is None
    assert get_recommendation_for_aqi(9999) is None
