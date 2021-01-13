from src.GraphInterface import GraphInterface


class NodeData:
    """This class represents a node in graph"""

    def __init__(self, key, pos: tuple = None, weight: float = 0):
        self.key = key
        self.pos = pos
        self.weight = weight
        self.tag = 0
        self.edges_in = {}
        self.edges_out = {}

    def __eq__(self, other):
        if self is None:
            return False
        if other is None or other.__class__ != self.__class__:
            return False
        return self.edges_out.keys().__eq__(other.edges_out.keys()) and self.edges_out.values().__eq__(
            other.edges_out.values())

    def __str__(self):
        return f"{self.key}"
        #if self.pos != ():
        #    return f"id: {self.key}, pos: {self.pos}"
        #else:
        #    return f"id: {self.key}"
#
    def __repr__(self):
        return f"{self.key}"
        #if self.pos is not None:
        #    return f"id: {self.key}, pos: {self.pos}"
        #else:
        #    return f"id: {self.key}"

    def __lt__(self, other):
        return self.weight < other.weight

    def __hash__(self):
        return hash(str(self))

    def to_json(self):
        try:
            if self.pos is None:
                return {"id": self.key}
            else:
                return {"id": self.key, "pos": f"{self.pos[0]},{self.pos[1]},{self.pos[2]}"}
        except Exception as e:
            print(e)


class DiGraph(GraphInterface):
    """This class represents a directed weighted graph """

    def __init__(self):
        self.vertex = {}
        self.__vertex_size = 0
        self.__edge_size = 0
        self.__mode_count = 0

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return self.__vertex_size

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return self.__edge_size

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return self.vertex

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        if id1 in self.vertex:
            return self.vertex.get(id1).edges_in
        else:
            return None

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        if id1 in self.vertex:
            return self.vertex.get(id1).edges_out
        else:
            return None

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.__mode_count

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.

        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if id1 in self.vertex and id2 in self.vertex:
            if id2 not in self.vertex.get(id1).edges_out:
                self.vertex.get(id1).edges_out[id2] = weight
                self.vertex.get(id2).edges_in[id1] = weight
                self.__edge_size += 1
                self.__mode_count += 1
                return True
        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.

        Note: if the node id already exists the node will not be added
        """
        if node_id in self.vertex:
            return False
        else:
            node_data = NodeData(key=node_id, pos=pos)
            self.vertex[node_id] = node_data
            self.__vertex_size += 1
            self.__mode_count += 1
            return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.

        Note: if the node id does not exists the function will do nothing
        """
        if node_id in self.vertex:
            if self.all_in_edges_of_node(node_id) is not None:
                for key in self.all_in_edges_of_node(node_id).keys():
                    self.vertex.get(key).edges_out.pop(node_id)
                    self.__edge_size -= 1
            if self.all_out_edges_of_node(node_id) is not None:
                for key in self.all_out_edges_of_node(node_id).keys():
                    self.vertex.get(key).edges_in.pop(node_id)
                    self.__edge_size -= 1
            self.vertex -= 1
            self.__mode_count += 1
            self.vertex.pop(node_id)
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.

        Note: If such an edge does not exists the function will do nothing
        """
        if node_id1 in self.vertex and node_id2 in self.vertex:
            if node_id2 in self.vertex.get(node_id1).edges_out:
                self.vertex.get(node_id1).edges_out.pop(node_id2)
                self.vertex.get(node_id2).edges_in.pop(node_id1)
                self.__mode_count += 1
                self.__edge_size -= 1
                return True

        return False

    def __eq__(self, other):
        if other is None or other.__class__ != self.__class__:
            return False
        return self.vertex.__eq__(other.vertex)

    def to_json(self) -> object:
        try:
            nodes = []
            edges = []
            json_dict = {}
            for node in self.get_all_v().values():
                if node.pos is None:
                    nodes.append({"id: ": node.key})
                else:
                    nodes.append({"id: ": node.key, "pos": f"{node.pos[0]},{node.pos[1]},{node.pos[2]}"})
            for key in self.vertex.keys():
                for dest, w in self.all_out_edges_of_node(key).items():
                    edges.append({"src": key, "dest": dest, "w": w})
            json_dict["Nodes"] = nodes
            json_dict["Edges"] = edges

        except Exception as e:
            print(e)
        return json_dict
