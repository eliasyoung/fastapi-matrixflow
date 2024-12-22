from fastapi import APIRouter
from app.schemas.matrix_flow import MatrixFlow, CreateMatrixFlowPayload, GetMatrixFlowResponse,GetMatrixFlowListItem
from app.crud.matrix_flow import create_matrix_flow, get_matrix_flow, get_all_matrix_flows, get_all_matrix_flows_list
from app.api.dep import DBSessoinDep

import json

router = APIRouter(prefix="/matrix_flow", tags=["matrix_flow"])

@router.get("/")
async def get_all_flows(db_session: DBSessoinDep):
    flows = await get_all_matrix_flows(db_session)
    return flows

@router.get("/flow_list", response_model=list[GetMatrixFlowListItem])
async def get_flow_list(db_session: DBSessoinDep):
    flow_list = await get_all_matrix_flows_list(db_session)
    return [GetMatrixFlowListItem.model_validate(row) for row in flow_list]

@router.get("/{flow_id}/detail", response_model=GetMatrixFlowResponse)
async def get_flow(flow_id: str, db_session: DBSessoinDep):
    flow = await get_matrix_flow(db_session, flow_id)
    graph_data = json.loads(flow.graph)

    return GetMatrixFlowResponse(
        id=flow.id, 
        graph=graph_data, 
        created_at=flow.created_at, 
        updated_at=flow.updated_at
    )

@router.post("/{flow_id}/save")
def save_flow(flow_id: str, flow: MatrixFlow):
    return {"flow": flow}

@router.post("/create", response_model=GetMatrixFlowResponse, status_code=201)
async def create_flow(flow: CreateMatrixFlowPayload, db_session: DBSessoinDep):
    new_flow = await create_matrix_flow(db_session, flow)
    await db_session.commit()
    await db_session.refresh(new_flow)

    graph_data = json.loads(new_flow.graph)

    return GetMatrixFlowResponse(
        id=new_flow.id,
        graph=graph_data,
        created_at=new_flow.created_at,
        updated_at=new_flow.updated_at
    )


