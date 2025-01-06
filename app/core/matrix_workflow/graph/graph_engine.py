from app.core.matrix_workflow.graph.graph import Graph
from app.core.matrix_workflow.nodes.node_type import NodeType
from app.core.matrix_workflow.nodes.node_type_class_mapping import node_type_class_mapping

class GraphEngine:

    def __init__(self, graph: Graph):
        self.graph = graph

    def run_graph(
        self,
    ):
        # edge_mapping = {
        #     key: [vars(edge) for edge in edge_list]
        #     for key, edge_list in self.graph.source_node_edge_mapping.items()
        # }

        start_node_id = self.graph.root_node_id
        # parallel_start_node_id = None
        next_node_id = start_node_id

        result_list = []

        while True:
            current_node_id = next_node_id

            current_node_config = self.graph.node_id_data_mapping.get(current_node_id)
            if not current_node_config:
                raise Exception(f"Run Error: node config of {current_node_id} not found!")


            current_node_type = NodeType(current_node_config.get("type"))
            current_node_cls = node_type_class_mapping[current_node_type]

            current_node_instance = current_node_cls()


            current_node_run_result = current_node_instance.run()
            result_list.append(current_node_run_result)


            if current_node_type == NodeType.END:
                break




            # get next node
            # TODO: CHECK PARALLEL
            edge_mappings = self.graph.source_node_edge_mapping.get(next_node_id)
            if not edge_mappings:
                break

            edge = edge_mappings[0]

            next_node_id = edge.target_node_id

            # if len(edge_mappings) == 1:
            #     edge = edge_mappings[0]

            #     next_node_id = edge.target_node_id







        # return {
        #     "root_node_id": start_node_id,
        #     "node_id_list": self.graph.node_id_list,
        #     "node_id_data_mapping": self.graph.node_id_data_mapping,
        #     "source_node_edge_mapping": edge_mapping
        # }
        return {
            "run_result": result_list
        }
