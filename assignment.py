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
    
def generate_keys():
  private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
  public_key = private_key.public_key()
  return private_key, public_key


def add_connection(from_user, to_user):
    # Add a directional connection between two users
    
    if not my_graph.has_edge(from_user, to_user):
        my_graph.add_edge(from_user, to_user)
        
def send_signed_message(sender, receiver, metadata, message_body):
  receiver_node = my_graph.nodes[receiver]
  
  recievers_public_key = receiver_node['public_key'] 
    
    
  message_signature = recievers_public_key.encrypt(
      message_body.encode(),
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
      )
    )
  
  print(f"Message from {sender} to {receiver} {metadata}: {message_signature}")
  return message_signature

def confirm_message(receiver, sender, message_signature, messagebody):
  receiver_private_key = my_graph.nodes[receiver]['private_key']
  
  decoded_signature = receiver_private_key.decrypt(       # Decode the signature into it's original text
      message_signature,
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
      )
  ).decode()
  
  if messagebody == decoded_signature:
    print("Signature from " + sender + " is correct")
  else:
    print("Incorrect signature")


        
def generate_keys():
  private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
  public_key = private_key.public_key()
  return private_key, public_key

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
    add_user("alice", {"real_name": "Aquantance Alice", "age": 30, "location": "Oahu"})
    add_user("bob", {"real_name": "Buddy Bob", "age": 25, "location": "Oahu"})
    add_user("eve", {"real_name": "Evil Eve", "age": 35, "location": "Oahu"})

    # Add connections
    add_connection("alice", "bob")
    add_connection("alice", "eve")

    add_connection("bob", "alice")

    add_connection("eve", "bob")

    messagebody = "Is this message signed?"
    message_signature = send_signed_message("alice", "bob", "Signed Message", messagebody)
    confirm_message("bob","alice", message_signature, messagebody)
    # Draw graph
    draw_graph()
