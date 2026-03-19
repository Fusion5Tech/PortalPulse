from fastapi import FastAPI

from app.api import auth_api, session_api, firewall_api, admin_api, vpn_api

app = FastAPI()

app.include_router(auth_api.router, prefix="/auth", tags=["auth"])
app.include_router(session_api.router, prefix="/sessions", tags=["sessions"])
app.include_router(firewall_api.router, prefix="/firewall", tags=["firewall"])
app.include_router(admin_api.router, prefix="/admin", tags=["admin"])
app.include_router(vpn_api.router, prefix="/vpn", tags=["vpn"])


@app.get("/")
def read_root():
    return {"message": "Welcome to PortalPulse"}
