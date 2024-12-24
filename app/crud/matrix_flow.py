from app.models import Matrixflow as MatrixFlowDBModel
from app.schemas.matrix_flow import CreateMatrixFlowPayload, UpdateMatrixFlowPayload
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

async def get_matrix_flow(db_session: AsyncSession, flow_id: uuid.UUID) -> MatrixFlowDBModel:
    flow = (await db_session.scalars(select(MatrixFlowDBModel).where(MatrixFlowDBModel.id == flow_id))).first()

    return flow



async def create_matrix_flow(db_session: AsyncSession, flow: CreateMatrixFlowPayload) -> MatrixFlowDBModel:
    insert_data = {key: value for key, value in flow.dict().items() if value is not None}
    graph = flow.graph.model_dump_json()
    insert_data.update({'graph': graph})

    result = await db_session.execute(insert(MatrixFlowDBModel).values(**insert_data).returning(MatrixFlowDBModel))

    new_flow = result.scalar_one()

    return new_flow

async def get_all_matrix_flows(db_session: AsyncSession):
    flows = (await db_session.scalars(select(MatrixFlowDBModel))).all()
    return flows

async def get_all_matrix_flows_list(db_session: AsyncSession):
    flow_list = (await db_session.execute(select(MatrixFlowDBModel.id, MatrixFlowDBModel.name, MatrixFlowDBModel.description, MatrixFlowDBModel.created_at, MatrixFlowDBModel.updated_at).order_by(MatrixFlowDBModel.created_at.desc()))).all()

    return flow_list

async def update_matrix_flow_by_id(db_session: AsyncSession, flow_id: uuid.UUID, flow_data: UpdateMatrixFlowPayload):
    update_data = {key: value for key, value in flow_data.dict().items() if value is not None}
    if flow_data.graph is not None:
        graph = flow_data.graph.model_dump_json()
        update_data.update({'graph': graph})

    updated_flow = (await db_session.scalars(update(MatrixFlowDBModel).where(MatrixFlowDBModel.id == flow_id).values(**update_data).returning(MatrixFlowDBModel))).first()

    return updated_flow
