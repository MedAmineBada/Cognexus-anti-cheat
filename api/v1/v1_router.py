"""
V1 API router configuration.
"""

from fastapi import APIRouter

from api.v1.routes.anti_cheat_routes import router as anti_cheat_router

router = APIRouter(prefix="/api/v1/anticheat")
router.include_router(anti_cheat_router)
