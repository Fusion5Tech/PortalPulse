from pydantic import BaseModel, Field, model_validator


class LoginRequest(BaseModel):
    """Api endpoint for login"""

    username: str | None = None
    password: str | None = None
    voucher_code: str | None = None
    ip_address: str | None = None
    mac_address: str | None = None
    device_name: str | None = None

    @model_validator(mode="after")
    def validate_auth_input(self) -> "LoginRequest":
        has_credentials = bool(self.username and self.password)
        has_voucher = bool(self.voucher_code)
        if has_credentials == has_voucher:
            raise ValueError(
                "Provide either username/password for admin login or voucher_code for user login"
            )
        return self


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str = Field(description="admin or voucher")
    session_id: str | None = None
