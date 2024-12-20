from fastapi import APIRouter
from app.schemas.matrix_flow import MatrixFlow

router = APIRouter(prefix="/matrix_flow", tags=["matrix_flow"])

@router.get("/{flow_id}")
def get_flow(flow_id: str):
    return {"flow": {
        "flow_id": flow_id
    }}

@router.post("/{flow_id}/save")
def save_flow(flow_id: str, flow: MatrixFlow):
    return {"flow": flow}
