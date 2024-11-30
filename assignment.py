import networkx as nx
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Initialize the graph
my_graph = nx.DiGraph()

def add_user(user_name, attributes = None):
    # Add a user to the social network

    if attributes is None:
        attributes = {}

    private_key, public_key = generate_keys()
    
    # Store public/private keys
    attributes['private_key'] = private_key
    attributes['public_key'] = public_key

    my_graph.add_node(user_name, **attributes)

def add_connection(from_user, to_user):
    # Add a directional connection between two users
    
    if not my_graph.has_edge(from_user, to_user):
        my_graph.add_edge(from_user, to_user)

def generate_keys():
  private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
  public_key = private_key.public_key()
  return private_key, public_key

def send_message(sender, receiver, message_body):
  sender_node = my_graph.nodes[sender]
  receiver_node = my_graph.nodes[receiver]

  public_key = receiver_node['public_key']
  encrypted_message = public_key.encrypt(
      message_body.encode(),
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
      )
  )
  
  print(f"Message from {sender} to {receiver} encrypted: {encrypted_message}")
  return encrypted_message

def decrypt_message(receiver, encrypted_message):
  private_key = my_graph.nodes[receiver]['private_key']
  decrypted_message = private_key.decrypt(
      encrypted_message,
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
      )
  ).decode()
  print(f"Message decrypted by {receiver}: {decrypted_message}")

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

    encrypted_msg = send_message("alice", "bob", "Hello Bob!")
    decrypt_message("bob", encrypted_msg)

    # Draw graph
    draw_graph()




