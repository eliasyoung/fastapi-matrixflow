from fastapi import APIRouter
from app.schemas.matrix_flow import CreateMatrixFlowPayload, GetMatrixFlowResponse,GetMatrixFlowListItem, UpdateMatrixFlowPayload
from app.crud.matrix_flow import create_matrix_flow, get_matrix_flow, get_all_matrix_flows, get_all_matrix_flows_list,update_matrix_flow_by_id
from app.api.dep import DBSessoinDep
import uuid
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
async def get_flow(flow_id: uuid.UUID, db_session: DBSessoinDep):
    flow = await get_matrix_flow(db_session, flow_id)
    graph_data = json.loads(flow.graph)

    return GetMatrixFlowResponse(
        id=flow.id,
        name=flow.name,
        description=flow.description,
        graph=graph_data,
        created_at=flow.created_at,
        updated_at=flow.updated_at
    )

@router.patch("/{flow_id}/save", response_model=GetMatrixFlowResponse)
async def save_flow(flow_id: uuid.UUID, flow: UpdateMatrixFlowPayload, db_session: DBSessoinDep):
    updated_flow = await update_matrix_flow_by_id(db_session, flow_id, flow)
    await db_session.commit()
    await db_session.refresh(updated_flow)

    graph_data = json.loads(updated_flow.graph)

    return GetMatrixFlowResponse(
        id=updated_flow.id,
        graph=graph_data,
        name=updated_flow.name,
        description=updated_flow.description,
        created_at=updated_flow.created_at,
        updated_at=updated_flow.updated_at
    )

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
