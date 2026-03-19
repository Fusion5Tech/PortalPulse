from fastapi import Depends
from app.utils.dependencies import get_current_user
from app.models.user_model import User
from app.services.vpn_service import VpnService
from fastapi import APIRouter

router = APIRouter()
vpn_service = VpnService()

@router.get("/check-vpn", response_model=dict)
async def check_vpn(ip_address: str, current_user: User = Depends(get_current_user)):
    return await vpn_service.check_vpn(ip_address)
