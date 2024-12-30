from fastapi import APIRouter, HTTPException
from app.schemas.matrix_workflow import (
    CreateMatrixWorkflowPayload,
    GetMatrixWorkflowResponse,
    GetMatrixWorkflowListItem,
    UpdateMatrixWorkflowPayload,
    MatrixWorkflowResponseGraph,
    # MatrixWorkflowNode
)
from app.schemas.api import CustomJSONResponse
from app.crud.matrix_workflow import (
    create_matrix_workflow,
    get_matrix_workflow,
    get_all_matrix_workflows,
    get_all_matrix_workflow_list,
    update_matrix_workflow_by_id,
    delete_matrix_workflow_by_id
)
from app.api.dep import DBSessoinDep

import uuid
import json

router = APIRouter(prefix="/matrix_workflow", tags=["matrix_workflow"])

@router.get("/")
async def get_all_workflows(db_session: DBSessoinDep):
    workflows = await get_all_matrix_workflows(db_session)
    return workflows

@router.get("/workflow_list", response_model=CustomJSONResponse[list[GetMatrixWorkflowListItem]])
async def get_workflow_list(db_session: DBSessoinDep):
    workflow_list = await get_all_matrix_workflow_list(db_session)

    return CustomJSONResponse(
        code=0,
        data=[GetMatrixWorkflowListItem.model_validate(row) for row in workflow_list]
    )

@router.get("/{workflow_id}/detail", response_model=CustomJSONResponse[GetMatrixWorkflowResponse])
async def get_workflow(workflow_id: uuid.UUID, db_session: DBSessoinDep):
    workflow = await get_matrix_workflow(db_session, workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    graph_data = json.loads(workflow.graph)

    return CustomJSONResponse(
        code=0,
        data=GetMatrixWorkflowResponse(
            id=workflow.id,
            name=workflow.name,
            description=workflow.description,
            graph=graph_data,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at
        )
    )

@router.patch("/{workflow_id}/save", response_model=CustomJSONResponse[GetMatrixWorkflowResponse])
async def save_workflow(workflow_id: uuid.UUID, workflow: UpdateMatrixWorkflowPayload, db_session: DBSessoinDep):
    updated_workflow = await update_matrix_workflow_by_id(db_session, workflow_id, workflow)

    if updated_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    await db_session.commit()
    await db_session.refresh(updated_workflow)

    graph_data = json.loads(updated_workflow.graph)

    return CustomJSONResponse(
        code=0,
        data=GetMatrixWorkflowResponse(
            id=updated_workflow.id,
            graph=graph_data,
            name=updated_workflow.name,
            description=updated_workflow.description,
            created_at=updated_workflow.created_at,
            updated_at=updated_workflow.updated_at
        )
    )

@router.post("/create", response_model=CustomJSONResponse[GetMatrixWorkflowResponse], status_code=201)
async def create_workflow(create_workflow_payload: CreateMatrixWorkflowPayload, db_session: DBSessoinDep):
    new_workflow = await create_matrix_workflow(db_session, create_workflow_payload)
    await db_session.commit()
    await db_session.refresh(new_workflow)

    graph_data = json.loads(new_workflow.graph)

    return CustomJSONResponse(
        code=0,
        data=GetMatrixWorkflowResponse(
            id=new_workflow.id,
            name=new_workflow.name,
            description=new_workflow.description,
            graph=graph_data,
            created_at=new_workflow.created_at,
            updated_at=new_workflow.updated_at
        )
    )

@router.post("/{workflow_id}/run")
async def run_workflow(workflow_id: uuid.UUID, db_session: DBSessoinDep):
    try:

        workflow = await get_matrix_workflow(db_session, workflow_id)


        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        graph = MatrixWorkflowResponseGraph.parse_raw(workflow.graph)

        # node_array = []

        # for node in graph.nodes:
        #     validated_node = MatrixFlowNode.validate(node)
        #     node_array.append(validated_node)


        return CustomJSONResponse(
            code=0,
            data=graph
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{workflow_id}/delete")
async def delete_workflow(workflow_id: uuid.UUID, db_session: DBSessoinDep):
    count = await delete_matrix_workflow_by_id(db_session, workflow_id)

    if count == 0:
        raise HTTPException(status_code=404, detail="Workflow not found")

    await db_session.commit()

    return CustomJSONResponse(
        code=0,
        data=None
    )
