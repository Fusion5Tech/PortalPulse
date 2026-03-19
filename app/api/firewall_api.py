from fastapi import APIRouter, Depends
from app.services.firewall_service import FirewallService
from app.schemas.firewall_schemas import FirewallRule
from app.models.user_model import User
from app.utils.dependencies import get_current_user

router = APIRouter()
firewall_service = FirewallService()

@router.post("/firewall/allow", response_model=FirewallRule)
async def allow_access(rule: FirewallRule, current_user: User = Depends(get_current_user)):
    return await firewall_service.allow_access(rule)

@router.post("/firewall/block", response_model=FirewallRule)
async def block_access(rule: FirewallRule, current_user: User = Depends(get_current_user)):
    return await firewall_service.block_access(rule)
