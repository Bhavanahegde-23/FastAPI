from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/")
async def read_auth():
    return {'user':'authenticated'}

