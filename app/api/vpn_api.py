from fastapi import APIRouter
from fastapi import Depends

from app.services.vpn_service import VpnService
from app.utils.dependencies import get_current_user

router = APIRouter()
vpn_service = VpnService()


@router.get("/check-vpn", response_model=dict)
async def check_vpn(ip_address: str, _current_user=Depends(get_current_user)):
    return await vpn_service.check_vpn(ip_address)
