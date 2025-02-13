#`src/graphql/resolvers/wifi_point.py`:
from math import ceil
from typing import List, Optional
from sqlalchemy import select, func
from geoalchemy2.functions import ST_DWithin
from src.database.session import get_session, AsyncSessionLocal
from src.models.wifi_point import WifiAccessPoint
from src.graphql.types.wifi_point import WifiAccessPointType, PaginatedWifiAccessPointType


async def get_wifi_points(
        page: int = 1,
        page_size: int = 10,
        neighborhood: str | None = None
) -> PaginatedWifiAccessPointType:
    async with AsyncSessionLocal() as session:  # Usar context manager directamente
        try:
            query = select(WifiAccessPoint)

            if neighborhood:
                query = query.where(WifiAccessPoint.neighborhood == neighborhood)

            # Primero ejecutar la consulta de count
            count_query = select(func.count()).select_from(WifiAccessPoint)
            if neighborhood:
                count_query = count_query.where(WifiAccessPoint.neighborhood == neighborhood)

            total_result = await session.execute(count_query)
            total = total_result.scalar() or 0

            # Luego la consulta principal con paginación
            query = query.offset((page - 1) * page_size).limit(page_size)
            result = await session.execute(query)
            items = result.scalars().all()

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
                total_pages=ceil(total / page_size) if total > 0 else 1
            )
        except Exception as e:
            print(f"Error in get_wifi_points: {e}")
            raise


async def get_wifi_point_by_id(id: str) -> Optional[WifiAccessPointType]:
    session = await anext(get_session())
    try:
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
    finally:
        await session.close()


async def get_wifi_points_by_proximity(
        latitude: float,
        longitude: float,
        radius: float = 1000,
        page: int = 1,
        page_size: int = 10
) -> PaginatedWifiAccessPointType:
    session = await anext(get_session())
    try:
        # Crear punto de referencia correctamente SIN ST_GeogFromText
        point = func.ST_MakePoint(longitude, latitude)  # Sin necesidad de GeogFromText

        query = select(WifiAccessPoint).where(
            func.ST_DWithin(
                WifiAccessPoint.location,
                func.ST_SetSRID(point, 4326),  # Convertir a SRID 4326
                radius
            )
        ).order_by(
            func.ST_Distance(WifiAccessPoint.location, func.ST_SetSRID(point, 4326))
        )

        # Contar total de registros
        total_query = select(func.count()).select_from(query.subquery().alias("total_subquery"))
        total_result = await session.execute(total_query)
        total = total_result.scalar() or 0  # Evitar None

        # Paginación
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
            total_pages=ceil(total / page_size) if total > 0 else 1
        )
    finally:
        await session.close()
