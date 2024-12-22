from fastapi import APIRouter
from app.schemas.matrix_flow import MatrixFlow, CreateMatrixFlowPayload
from app.crud.matrix_flow import create_matrix_flow, get_matrix_flow, get_all_matrix_flows
from app.api.dep import DBSessoinDep

import logging

router = APIRouter(prefix="/matrix_flow", tags=["matrix_flow"])

@router.get("/")
async def get_all_flows(db_session: DBSessoinDep):
    flows = await get_all_matrix_flows(db_session)
    return flows

@router.get("/{flow_id}")
async def get_flow(flow_id: str, db_session: DBSessoinDep):
    flow = await get_matrix_flow(db_session, flow_id)
    return flow

@router.post("/{flow_id}/save")
def save_flow(flow_id: str, flow: MatrixFlow):
    return {"flow": flow}

@router.post("/create")
async def create_flow(flow: CreateMatrixFlowPayload, db_session: DBSessoinDep):
    new_flow = await create_matrix_flow(db_session, flow)
    await db_session.commit()
    await db_session.refresh(new_flow)
    return {"flow": new_flow}
