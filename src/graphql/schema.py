# src/graphql/schema.py
import strawberry
from typing import List, Optional
from .types.wifi_point import (
    WifiAccessPointType,
    PaginatedWifiAccessPointType,
    LocationInput
)
from .resolvers.wifi_point import (
    get_wifi_points,
    get_wifi_point_by_id,
    get_wifi_points_by_proximity
)

@strawberry.type
class Query:
    @strawberry.field
    async def wifi_points(
        self,
        page: int = 1,
        page_size: int = 10,
        neighborhood: str | None = None
    ) -> PaginatedWifiAccessPointType:
        return await get_wifi_points(page, page_size, neighborhood)

    @strawberry.field
    async def wifi_point(
        self,
        id: str
    ) -> Optional[WifiAccessPointType]:
        return await get_wifi_point_by_id(id)

    @strawberry.field
    async def wifi_points_by_proximity(
        self,
        location: LocationInput,
        page: int = 1,
        page_size: int = 10
    ) -> PaginatedWifiAccessPointType:
        return await get_wifi_points_by_proximity(
            location.latitude,
            location.longitude,
            location.radius,
            page,
            page_size
        )

schema = strawberry.Schema(query=Query)