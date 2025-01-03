from app.core.matrix_workflow.nodes.node_type import NodeType
from app.core.matrix_workflow.nodes.base.base_node import BaseNode

class AddNode(BaseNode):
    _node_type = NodeType.ADD

    def _run(self) -> str:
        return self._node_type
