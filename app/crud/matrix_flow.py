from app.models import Matrixflow as MatrixFlowDBModel
from app.schemas.matrix_flow import CreateMatrixFlowPayload
from fastapi import HTTPException
from sqlalchemy import select, insert
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

async def get_all_matrix_flows(db_session: AsyncSession) -> list[uuid.UUID]:
    flow_ids = (await db_session.scalars(select(MatrixFlowDBModel.id))).all()
    return flow_ids