from datetime import datetime
from typing import Optional, Any
from geoalchemy2.shape import to_shape
from sqlmodel import SQLModel, Field
from geoalchemy2 import Geography, WKTElement
from shapely.geometry import Point
from sqlalchemy import Column

class WifiAccessPointBase(SQLModel):
    """Base model for WiFi access points"""
    model_config = {"arbitrary_types_allowed": True}

    program: str = Field(index=True)
    installation_date: Optional[datetime] = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    neighborhood: str = Field(index=True)
    district: str = Field(index=True)


class WifiAccessPoint(WifiAccessPointBase, table=True):
    """Database model for WiFi access points"""
    __tablename__ = "wifi_access_points"

    id: Optional[str] = Field(default=None, primary_key=True)
    location: Optional[WKTElement] = Field(
        sa_column=Column(
            Geography(geometry_type='POINT', srid=4326, spatial_index=True),
            nullable=True
        )
    )
    def set_location(self):
        """Sets the geographic point based on latitude and longitude"""
        self.location = f'SRID=4326;POINT({self.longitude} {self.latitude})'

    def get_coordinates(self) -> tuple[float, float]:
        """Returns the latitude and longitude from the location field"""
        if self.location:
            point = to_shape(self.location)
            return (point.y, point.x)  # latitude, longitude
        return (self.latitude, self.longitude)


class WifiAccessPointCreate(WifiAccessPointBase):
    """Create model for WiFi access points"""
    pass


class WifiAccessPointRead(WifiAccessPointBase):
    """Update model for WiFi access points"""
    id: str


class WifiAccessPointUpdate(SQLModel):
    """Schema for updating a WiFi access point"""
    program: Optional[str] = None
    installation_date: Optional[datetime] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    neighborhood: Optional[str] = None
    district: Optional[str] = None
