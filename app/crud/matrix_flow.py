from app.models import Matrixflow as MatrixFlowDBModel
from app.schemas.matrix_flow import CreateMatrixFlowPayload, UpdateMatrixFlowPayload
from fastapi import HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

async def get_matrix_flow(db_session: AsyncSession, flow_id: uuid.UUID) -> MatrixFlowDBModel:
    flow = (await db_session.scalars(select(MatrixFlowDBModel).where(MatrixFlowDBModel.id == flow_id))).first()
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    return flow



async def create_matrix_flow(db_session: AsyncSession, flow: CreateMatrixFlowPayload) -> MatrixFlowDBModel:
    graph = flow.model_dump_json()

    result = await db_session.execute(insert(MatrixFlowDBModel).values(graph=graph).returning(MatrixFlowDBModel))

    new_flow = result.scalar_one()

    return new_flow

async def get_all_matrix_flows(db_session: AsyncSession):
    flows = (await db_session.scalars(select(MatrixFlowDBModel))).all()
    return flows

async def get_all_matrix_flows_list(db_session: AsyncSession):
    flow_list = (await db_session.execute(select(MatrixFlowDBModel.id, MatrixFlowDBModel.created_at, MatrixFlowDBModel.updated_at))).all()

    return flow_list

async def update_matrix_flow_by_id(db_session: AsyncSession, flow_id: uuid.UUID, flow_data: UpdateMatrixFlowPayload):
    update_data = {key: value for key, value in flow_data.dict().items() if value is not None}
    if flow_data.graph is not None:
        graph = flow_data.graph.model_dump_json()
        update_data.update({'graph': graph})

    updated_flow = (await db_session.scalars(update(MatrixFlowDBModel).where(MatrixFlowDBModel.id == flow_id).values(**update_data).returning(MatrixFlowDBModel))).first()

    if updated_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")

    return updated_flow
