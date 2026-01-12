from fastapi import APIRouter, File, UploadFile, Form
from ..models import TryOnResult

router = APIRouter(prefix="/try-on", tags=["Virtual Try-On"])

@router.post("/", response_model=TryOnResult)
async def try_on(
    userImage: UploadFile = File(...),
    productId: int = Form(...)
):
    # Mock implementation
    # In a real app, we would process the image here
    return {"result_image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZmFzaGlvbiUyMG1vZGVsfGVufDB8fDB8fHww"}
