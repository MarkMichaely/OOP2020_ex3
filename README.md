# OOP2020_ex3

![alt text](https://ucarecdn.com/d624d487-da51-42ad-a520-cc3fb8f253bd/)
## what is this?
An implementation of directional weighted graph in Python.
It is able to calculate and retrieve the shortest path from any node on the graph by using Dijkstra's algorithm.
Also, the program is able to compute the strongly connected componenets of the graph, either for one node and it's connected componenets or the entire graph's
The program is able to save any created graph to JSON file and is also able to load a graph from JSON.


**Links:**
* https://networkx.org/
* https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
* https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
* https://matplotlib.org/
* https://numpy.org/


**Classes in project:**

**DiGraph**
this class represents the graph itself, with this class and it's methods we are able to:
* create graphs
* add nodes
* remove nodes
* add edges
* remove edges
* know how many edges and nodes are in a graph in any given time

**DiGraph methods**

* `v_size(self)` method to return the number of vertices in the graph, returnes an Integer
* `e_size(self)` method to return the number of edges in the graph, returnes an Integer
* `get_all_v(self)` returnes a dictionary of all the nodes in the graph, each node is represented using a pair (node_id, node_data)
* `all_in_edges_of_node(self, id1: int)` return a dictionary of all the nodes connected to (into) node_id ,each node is represented using a pair (other_node_id, weight)
* `all_out_edges_of_node(self, id1: int)` return a dictionary of all the nodes connected from node_id , each node is represented using a pair (other_node_id, weight)
* `get_mc(self)` method returns integer representing the current version of graph, each change in the state of the graph should change this number
* `add_node(self, node_id: int, pos: tuple)` method adds node to graph with node_id as it's key and pos and it's postion, if not given position add node without one
* `add_edge(self, id1: int, id2: int, weight: float)` method adds an edge from node with key od id1 to node with key of id2 with weight representing the weight of this edge
* `to_json(self)` method to write graph in JSON format

**GraphAlgo**
this class represents the algorithems on directed weighted graph, it recieves a DiGraph object and is able to:
* load and save graphs in JSON file
* compute the shortest path of two nodes in graph and return a path as well as it's weight
* compute the strongly connected components(SCC) of grpah and return a list of all SCC in graph or a list of SCC of single node
* draw graphs using mathplotlib library

**GraphAlgo methods**

* `get_graph(self)` method to return the graph that the alogirthm works on
* `load_from_json(self, file_name: str)` method to load a graph from an existing JSON file. file_name is directorty path.
* `save_to_json(self, file_name: str)` method is used to save the graph to JSON file. file_name is directorty path
* `shortest_path(self, id1: int, id2: int)` Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm in pair (shortest path weight, path)
* `connected_component(self, id1: int)` returns list of SCC of that node id1 is a part of
* `connected_components(self)`  Finds all the Strongly Connected Component(SCC) in the graph and returns list of lists
* `plot_graph(self)` draws graph using mathplotlib library


