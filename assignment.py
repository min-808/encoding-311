import networkx as nx
import matplotlib.pyplot as plt

# Initialize the graph
my_graph = nx.DiGraph()

def add_user(user_name, attributes = None):
    # Add a user to the social network

    if attributes is None:
        attributes = {}
    my_graph.add_node(user_name)

def add_connection(from_user, to_user):
    # Add a directional connection between two users
    
    if not my_graph.has_edge(from_user, to_user):
        my_graph.add_edge(from_user, to_user)

def draw_graph():
    # Draw the graph using matplotlib
    plt.figure(figsize=(16, 10))
    
    # Node positions
    pos = nx.spring_layout(my_graph)
    
    # Draw nodes and edges
    nx.draw_networkx_nodes(my_graph, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_edges(my_graph, pos, arrowstyle="->", arrowsize=30, edge_color='black')
    
    # Node labels
    node_labels = {node: node for node in my_graph.nodes()}
    nx.draw_networkx_labels(my_graph, pos, labels=node_labels, font_size=8, font_color='black')

    # Display the graph
    plt.title("Example Graph")
    plt.axis("off")
    plt.show()
 
# Example usage
if __name__ == "__main__":
    # Add users
    add_user("alice", {"real_name": "Alice Smith", "age": 30, "location": "Oahu"})
    add_user("bob", {"real_name": "Bob Jones", "age": 25, "location": "Oahu"})
    add_user("carol", {"real_name": "Carol White", "age": 35, "location": "Oahu"})

    # Add connections
    add_connection("alice", "bob")
    add_connection("alice", "carol")

    add_connection("bob", "alice")

    add_connection("carol", "bob")

    # Draw graph
    draw_graph()