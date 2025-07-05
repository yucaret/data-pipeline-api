from fastapi import APIRouter

router = APIRouter()

@router.post("/batch")
def insert_batch():
    return {"message": "Batch insert endpoint ready"}
