import pytest
from src.models.wifi_point import WifiAccessPoint


def test_wifi_access_point_creation():
    """Verifica que se puede crear un objeto WifiAccessPoint correctamente."""
    wifi = WifiAccessPoint(
        id="TEST001",
        program="Test Program",
        latitude=19.4326,
        longitude=-99.1332,
        neighborhood="Centro",
        district="CDMX"
    )

    assert wifi.id == "TEST001"
    assert wifi.program == "Test Program"
    assert wifi.latitude == 19.4326
    assert wifi.longitude == -99.1332
    assert wifi.neighborhood == "Centro"
    assert wifi.district == "CDMX"
