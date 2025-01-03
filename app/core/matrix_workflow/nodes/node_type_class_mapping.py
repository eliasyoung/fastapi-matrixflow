from app.core.matrix_workflow.nodes.node_type import NodeType

from app.core.matrix_workflow.nodes.base.base_node import BaseNode
from app.core.matrix_workflow.nodes.start.start_node import StartNode
from app.core.matrix_workflow.nodes.end.end_node import EndNode
from app.core.matrix_workflow.nodes.add.add_node import AddNode

node_type_class_mapping: dict[NodeType, type[BaseNode]] = {
    NodeType.START: StartNode,
    NodeType.END: EndNode,
    NodeType.ADD: AddNode
}
