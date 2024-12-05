import networkx as nx
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.hashes import SHA256
import base64
import json

# Initialize the graph
my_graph = nx.DiGraph()

# Function to generate RSA keys
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

# add_user function
def add_user(user_name, attributes=None):
    if attributes is None:
        attributes = {}
    private_key, public_key = generate_keys()
    attributes['private_key'] = private_key
    attributes['public_key'] = public_key
    my_graph.add_node(user_name, **attributes)

def add_connection(from_user, to_user):
    if not my_graph.has_edge(from_user, to_user):
        my_graph.add_edge(from_user, to_user)

def hash_message(message_body):
    digest = hashes.Hash(SHA256())
    digest.update(message_body.encode())
    return digest.finalize()

def send_signed_message(sender, receiver, message_body):
    sender_node = my_graph.nodes[sender]
    private_key = sender_node['private_key']
    message_hash = hash_message(message_body)

    signature = private_key.sign(
        message_hash,
        padding.PSS(
            mgf=padding.MGF1(SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        SHA256()
    )

    print(f"Signed message from {sender} to {receiver} sent.")
    return {"message_body": message_body, "signature": signature, "hash": message_hash}

def validate_signed_message(sender, signed_message):
    sender_node = my_graph.nodes[sender]
    public_key = sender_node['public_key']  # Use the sender's public key

    try:
        public_key.verify(
            signed_message['signature'],
            signed_message['hash'],
            padding.PSS(
                mgf=padding.MGF1(SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            SHA256()
        )
        print(f"Message from {sender} validated successfully.")
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False

def respond_to_signed_message(sender, receiver, signed_message):
    if not validate_signed_message(sender, signed_message):  # Pass the sender
        print("Invalid signed message. Response aborted.")
        return None

    original_hash = signed_message['hash']
    response_body = f"Message received and validated by {receiver}."
    response_hash = hash_message(response_body)

    private_key = my_graph.nodes[receiver]['private_key']
    response_signature = private_key.sign(
        response_hash,
        padding.PSS(
            mgf=padding.MGF1(SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        SHA256()
    )

    response = {
        "original_signature": base64.b64encode(signed_message['signature']).decode('utf-8'),
        "original_hash": base64.b64encode(original_hash).decode('utf-8'),
        "response_body": response_body,
        "response_hash": base64.b64encode(response_hash).decode('utf-8'),
        "response_signature": base64.b64encode(response_signature).decode('utf-8')
    }

    print(f"Response from {receiver} to {sender} signed and sent.")
    print(json.dumps(response, indent=4))  # Pretty-print the response
    return response

# Testing
if __name__ == "__main__":
    # Example graph setup
    add_user("alice", {"real_name": "Alice Smith", "age": 30, "location": "Oahu"})
    add_user("bob", {"real_name": "Bob Jones", "age": 25, "location": "Oahu"})
    add_user("carol", {"real_name": "Carol White", "age": 35, "location": "Oahu"})

    add_connection("alice", "bob")
    add_connection("bob", "alice")
    add_connection("alice", "carol")

    # Send and respond to a signed message
    message_to_bob = send_signed_message("alice", "bob", "Hello Bob!")
    response_from_bob = respond_to_signed_message("alice", "bob", message_to_bob)

    if response_from_bob:
        print("Final Response:")
        print(json.dumps(response_from_bob, indent=4))
