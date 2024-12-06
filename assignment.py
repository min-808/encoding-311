import datetime
import json
import networkx as nx
import matplotlib.pyplot as plt

# Initialize the graph
my_graph = nx.DiGraph()

def add_user(user_name, attributes = None):
    # Add a user to the social network

    if attributes is None:
        attributes = {}
    my_graph.add_node(user_name, messages=[])

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
    
    # Draw graph
    draw_graph()

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
    

def sendCompressedMessage(sender, receiver, message):
    """
    Compresses a message using Run Length Encoding and sends it
    with the appropriate metadata.
    """
    if sender not in my_graph.nodes or receiver not in my_graph.nodes:
        raise ValueError("Sender or receiver does not exist in the graph.")
    
    # Run Length Encode Function
    def runLengthEncode(message):
        if not message:
            return ""
        
        encodedMessage = []
        count = 1

        for i in range(1, len(message)):
            if message[i] == message[i - 1]:
                count += 1
            else:
                encodedMessage.append(f"{count}{message[i - 1]}")
                count = 1
        
        # Add the last group
        encodedMessage.append(f"{count}{message[-1]}")
        
        return ''.join(encodedMessage)

    
    # Compress the message
    compressedMessage = runLengthEncode(message)
    
    now = str(datetime.datetime.now())
    # Create metadata to be stored in the message
    metadata = {"compression":"run-length","sender":sender,"receiver":receiver,"timestamp":now}
    
    # Create the message content to be stored in the sender's messages
    messageContent = {"metadata":metadata,"message body":compressedMessage}
    
    # Add the message to the sender's messages
    my_graph.nodes[sender]["messages"].append(messageContent)
    # Add the message to the receiver's messages
    my_graph.nodes[receiver]["messages"].append(messageContent)
    
    return messageContent
  
def decompressMessage(message):
    """
    Decompresses a message that was compressed using Run Length Encoding.
    """
    if not message:
        return ""
    
    decodedMessage = []
    count = ""
    
    for char in message:
        if char.isdigit():
            count += char  # Accumulate digits for count
        else:
            decodedMessage.append(char * int(count))  # Repeat character
            count = ""  # Reset count
    
    return ''.join(decodedMessage)
  
def getMessages(user):
    """
    Returns all messages for a user.
    """
    if user not in my_graph.nodes:
        raise ValueError("User does not exist in the graph.")
    
    return my_graph.nodes[user]["messages"]
  
# Example usage

# Send a compressed message from alice to bob
messageContent = sendCompressedMessage("alice", "bob", "Super Secret Message abbcccddddeeeeeffffff")
print(messageContent)

# Decompress the message
decompressedMessage = decompressMessage(messageContent["messageBody"])
print(decompressedMessage)

# Get all messages for bob
messages = getMessages("bob")
print(messages)
    