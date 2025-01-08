from abc import abstractmethod
from app.core.matrix_workflow.nodes.node_type import NodeType
from app.core.matrix_workflow.workflow_runner.variables.variable_pool import VariablePool


class BaseNode:
    _node_type: NodeType

    def __init__(self, variable_pool: VariablePool):
        self.variable_pool = variable_pool

    @abstractmethod
    def _run(self) -> str:
        raise NotImplementedError

    def run(self) -> str:
        return self._run()
