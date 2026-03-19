from app.api import vpn_api
from app.main import app

app.include_router(vpn_api.router, prefix="/vpn", tags=["vpn"])
