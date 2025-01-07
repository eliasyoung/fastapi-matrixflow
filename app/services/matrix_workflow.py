import uuid

from app.api.dep import DBSessoinDep
from app.crud.matrix_workflow import (
    get_matrix_workflow
)
from app.schemas.matrix_workflow import MatrixWorkflowGraph
from app.core.matrix_workflow.graph.graph import Graph
from app.core.matrix_workflow.graph.graph_engine import GraphEngine


class MatrixWorkflowRunningService:

    @classmethod
    async def run(cls, db_session: DBSessoinDep, workflow_id: uuid.UUID):
        workflow = await get_matrix_workflow(db_session, workflow_id)

        if not workflow:
            raise Exception("Workflow not found")

        graph = MatrixWorkflowGraph.parse_raw(workflow.graph)
        graph_cls_instance = Graph.init(graph.dict())
        graph_engine = GraphEngine(graph=graph_cls_instance)
        running_result = graph_engine.run_graph()

        return running_result
