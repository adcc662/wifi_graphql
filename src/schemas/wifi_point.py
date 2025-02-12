from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, validator

class Location(BaseModel):
    """Schema for geographic location"""
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

class WifiAccessPointBase(BaseModel):
    """Base schema for WiFi access points"""
    model_config = ConfigDict(from_attributes=True)

    program: str = Field(min_length=1, max_length=100)
    installation_date: datetime
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    neighborhood: str = Field(min_length=1, max_length=100)
    district: str = Field(min_length=1, max_length=100)

    @validator('installation_date')
    def validate_installation_date(cls, v):
        if v > datetime.now():
            raise ValueError("Installation date cannot be in the future")
        return v

class WifiAccessPointCreate(WifiAccessPointBase):
    """Schema for creating WiFi access points"""
    pass

class WifiAccessPointUpdate(BaseModel):
    """Schema for updating WiFi access points"""
    model_config = ConfigDict(from_attributes=True)

    program: Optional[str] = None
    installation_date: Optional[datetime] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    neighborhood: Optional[str] = None
    district: Optional[str] = None

class WifiAccessPointInDBBase(WifiAccessPointBase):
    """Base schema for WiFi access points in database"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class WifiAccessPoint(WifiAccessPointInDBBase):
    """Complete schema for WiFi access points"""
    pass

class PaginatedWifiAccessPoint(BaseModel):
    """Schema for paginated response"""
    model_config = ConfigDict(from_attributes=True)

    items: List[WifiAccessPoint]
    total: int
    page: int
    page_size: int
    total_pages: int

class ProximitySearch(BaseModel):
    """Schema for proximity search parameters"""
    model_config = ConfigDict(from_attributes=True)

    location: Location
    radius: float = Field(gt=0, default=1000)  # Radio en metros

class ResponseMessage(BaseModel):
    """Schema for API response messages"""
    message: str
    details: Optional[str] = None