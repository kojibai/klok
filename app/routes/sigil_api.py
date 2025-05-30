# routes/sigil_api.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.routes.klock_utils import get_kairos_data_for_sigil


router = APIRouter()


@router.get("/sigil/live", summary="Generate live sigil metadata", tags=["Sigil"])
async def generate_live_sigil():
    """
    Endpoint that returns harmonic Kairos data for live sigil generation.
    """
    try:
        sigil_data = get_kairos_data_for_sigil()
        return JSONResponse(content={"success": True, "data": sigil_data})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500
        )
