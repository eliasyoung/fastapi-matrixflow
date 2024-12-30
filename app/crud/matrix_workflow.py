from app.models import MatrixWorkflow as MatrixWorkflowDBModel
from app.schemas.matrix_workflow import CreateMatrixWorkflowPayload, UpdateMatrixWorkflowPayload
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

async def get_matrix_workflow(db_session: AsyncSession, workflow_id: uuid.UUID) -> MatrixWorkflowDBModel:
    workflow = (await db_session.scalars(select(MatrixWorkflowDBModel).where(MatrixWorkflowDBModel.id == workflow_id))).first()

    return workflow



async def create_matrix_workflow(db_session: AsyncSession, create_workflow_payload: CreateMatrixWorkflowPayload) -> MatrixWorkflowDBModel:
    insert_data = {key: value for key, value in create_workflow_payload.dict().items() if value is not None}
    graph = create_workflow_payload.graph.model_dump_json()
    insert_data.update({'graph': graph})

    result = await db_session.execute(insert(MatrixWorkflowDBModel).values(**insert_data).returning(MatrixWorkflowDBModel))

    new_workflow = result.scalar_one()

    return new_workflow

async def get_all_matrix_workflows(db_session: AsyncSession):
    workflows = (await db_session.scalars(select(MatrixWorkflowDBModel))).all()
    return workflows

async def get_all_matrix_workflow_list(db_session: AsyncSession):
    workflow_list = (await db_session.execute(select(MatrixWorkflowDBModel.id, MatrixWorkflowDBModel.name, MatrixWorkflowDBModel.description, MatrixWorkflowDBModel.created_at, MatrixWorkflowDBModel.updated_at).order_by(MatrixWorkflowDBModel.created_at.desc()))).all()

    return workflow_list

async def update_matrix_workflow_by_id(db_session: AsyncSession, workflow_id: uuid.UUID, workflow_data: UpdateMatrixWorkflowPayload):
    update_data = {key: value for key, value in workflow_data.dict().items() if value is not None}
    if workflow_data.graph is not None:
        graph = workflow_data.graph.model_dump_json()
        update_data.update({'graph': graph})

    updated_workflow = (await db_session.scalars(update(MatrixWorkflowDBModel).where(MatrixWorkflowDBModel.id == workflow_id).values(**update_data).returning(MatrixWorkflowDBModel))).first()

    return updated_workflow

async def delete_matrix_workflow_by_id(db_session: AsyncSession, workflow_id: uuid.UUID):
    result = (await db_session.execute(delete(MatrixWorkflowDBModel).where(MatrixWorkflowDBModel.id == workflow_id)))

    return result.rowcount
