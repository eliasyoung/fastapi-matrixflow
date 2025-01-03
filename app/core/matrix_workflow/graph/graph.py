from typing import Any, cast
from pydantic import BaseModel
from app.core.matrix_workflow.nodes.node_type import NodeType

class Edge:
    target_node_id: str
    source_node_id: str

    def __init__(self, target_node_id: str, source_node_id: str):
        self.target_node_id = target_node_id
        self.source_node_id = source_node_id


class Graph:

    # node_list: list[Any]=[]
    # edge_list: list[Any]=[]

    root_node_id: str
    node_id_list: list[str]=[]
    node_id_data_mapping: dict[str, dict]={}
    source_node_edge_mapping: dict[str, list[Edge]]={}

    @classmethod
    def init(cls, graph_data: dict[str, Any]) -> "Graph":
        node_list = graph_data.get("nodes")
        edge_list = graph_data.get("edges")
        if node_list is None or edge_list is None:
            raise Exception('Nodes or Edges not found in Graph')

        node_list = cast(list[dict[str, Any]], node_list)
        edge_list = cast(list[dict[str, Any]], edge_list)

        source_node_edge_mapping={}

        graph = cls()

        for edge in edge_list:
            source_node_id = edge.get("source")
            target_node_id = edge.get("target")

            if not source_node_id or not target_node_id:
                continue

            if source_node_id not in source_node_edge_mapping:
                source_node_edge_mapping[source_node_id] = []

            new_edge = Edge(target_node_id=target_node_id, source_node_id=source_node_id)

            source_node_edge_mapping[source_node_id].append(new_edge)


        graph.source_node_edge_mapping = source_node_edge_mapping

        for node in node_list:
            if node["type"] == NodeType.START:
                graph.root_node_id = node["id"]

            graph.node_id_list.append(node["id"])
            graph.node_id_data_mapping.update({node["id"]: node})


        return graph
