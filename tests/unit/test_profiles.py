import pytest

from plkg.radio.profiles import get_profile, list_profiles


def test_profiles_separate_csi_from_rssi() -> None:
    assert get_profile("nr_fr1_n78").measurement == "csi"
    assert get_profile("iot_static_sensor").measurement == "rssi"


def test_all_packaged_profiles_are_loadable() -> None:
    names = list_profiles()

    assert names == (
        "iot_static_sensor",
        "iot_wearable",
        "nr_fr1_n78",
        "nr_mmwave_n257",
        "six_g_sub_thz_research",
    )
    assert all(get_profile(name).name == name for name in names)


def test_unknown_profile_is_rejected() -> None:
    with pytest.raises(ValueError):
        get_profile("unknown")
