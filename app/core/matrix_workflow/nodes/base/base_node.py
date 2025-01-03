from abc import abstractmethod
from app.core.matrix_workflow.nodes.node_type import NodeType


class BaseNode:
    _node_type: NodeType

    @abstractmethod
    def _run(self) -> str:
        raise NotImplementedError

    def run(self) -> str:
        return self._run()
