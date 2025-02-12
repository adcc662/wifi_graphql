from math import ceil
from typing import List, Optional
from sqlalchemy import select, func
from geoalchemy2.functions import ST_DWithin, ST_MakePoint
from src.database.session import get_session
from src.models.wifi_point import WifiAccessPoint
from src.graphql.types.wifi_point import WifiAccessPointType, PaginatedWifiAccessPointType


async def get_wifi_points(
        page: int = 1,
        page_size: int = 10
) -> PaginatedWifiAccessPointType:
    async with get_session() as session:
        query = select(WifiAccessPoint)
        total = await session.execute(select(func.count()).select_from(WifiAccessPoint))
        total = total.scalar()

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await session.execute(query)
        items = result.scalars().all()

        # Convertir a tipos GraphQL
        wifi_points = [
            WifiAccessPointType(
                id=item.id,
                program=item.program,
                installation_date=item.installation_date,
                latitude=item.latitude,
                longitude=item.longitude,
                neighborhood=item.neighborhood,
                district=item.district
            ) for item in items
        ]

        return PaginatedWifiAccessPointType(
            items=wifi_points,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=ceil(total / page_size)
        )


async def get_wifi_point_by_id(id: str) -> Optional[WifiAccessPointType]:
    async with get_session() as session:
        result = await session.execute(
            select(WifiAccessPoint).where(WifiAccessPoint.id == id)
        )
        item = result.scalar_one_or_none()
        if item is None:
            return None

        return WifiAccessPointType(
            id=item.id,
            program=item.program,
            installation_date=item.installation_date,
            latitude=item.latitude,
            longitude=item.longitude,
            neighborhood=item.neighborhood,
            district=item.district
        )


async def get_wifi_points_by_proximity(
        latitude: float,
        longitude: float,
        radius: float = 1000,
        page: int = 1,
        page_size: int = 10
) -> PaginatedWifiAccessPointType:  # Cambiado el tipo de retorno
    async with get_session() as session:
        # Crear punto de referencia con SRID 4326 (WGS84)
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

        query = select(WifiAccessPoint).where(
            func.ST_DWithin(
                WifiAccessPoint.location,
                point,
                radius,
                use_spheroid=True  # Para cálculos más precisos
            )
        ).order_by(  # Ordenar por distancia
            func.ST_Distance(WifiAccessPoint.location, point)
        )

        total = await session.execute(select(func.count()).select_from(query.subquery()))
        total = total.scalar()

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await session.execute(query)
        items = result.scalars().all()

        # Convertir a tipos GraphQL
        wifi_points = [
            WifiAccessPointType(
                id=item.id,
                program=item.program,
                installation_date=item.installation_date,
                latitude=item.latitude,
                longitude=item.longitude,
                neighborhood=item.neighborhood,
                district=item.district
            ) for item in items
        ]

        return PaginatedWifiAccessPointType(  # Cambiado el tipo de retorno
            items=wifi_points,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=ceil(total / page_size)
        )