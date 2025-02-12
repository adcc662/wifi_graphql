import strawberry
from datetime import datetime
from typing import List, Optional

@strawberry.type
class GeoLocation:
    latitude: float
    longitude: float

@strawberry.input
class LocationInput:
    latitude: float
    longitude: float
    radius: float = 1000.0  # metros por defecto

@strawberry.type
class WifiAccessPointType:
    id: str
    program: str
    installation_date: datetime
    latitude: float
    longitude: float
    neighborhood: str
    district: str

@strawberry.type
class PaginatedWifiAccessPointType:
    items: List[WifiAccessPointType]
    total: int
    page: int
    page_size: int
    total_pages: int