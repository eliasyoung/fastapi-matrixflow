import uuid
from typing import Mapping, Any

from app.api.dep import DBSessoinDep
from app.crud.matrix_workflow import (
    get_matrix_workflow
)
from app.schemas.matrix_workflow import MatrixWorkflowGraph
from app.core.matrix_workflow.graph.graph import Graph
from app.core.matrix_workflow.graph.graph_engine import GraphEngine
from app.core.matrix_workflow.workflow_runner.runner import MatrixWorkflowRunner


class MatrixWorkflowRunningService:

    @classmethod
    async def run(cls, db_session: DBSessoinDep, workflow_id: uuid.UUID, inputs_vars: Mapping[str, Any]):


        runner = MatrixWorkflowRunner(inputs_vars=inputs_vars, workflow_id=workflow_id, db_session=db_session)
        result = await runner.run()

        return result
