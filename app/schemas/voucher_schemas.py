from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VoucherCreateRequest(BaseModel):
    count: int = Field(default=1, ge=1, le=200)
    duration_minutes: int = Field(default=60, ge=1, le=24 * 60)


class VoucherOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    duration_minutes: int
    is_active: bool
    is_used: bool
    printed: bool
    created_at: datetime
    expires_at: datetime | None = None
    used_at: datetime | None = None


class VoucherPrintItem(BaseModel):
    code: str
    duration_minutes: int


class VoucherPrintResponse(BaseModel):
    vouchers: list[VoucherPrintItem]
    printable_text: str
