from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
def upload_csv():
    return {"message": "Upload endpoint ready"}
