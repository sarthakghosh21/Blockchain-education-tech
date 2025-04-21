import streamlit as st
from PIL import Image, ImageDraw
import os
import hashlib
import random
import json
from time import time
import wolframalpha

# Initialize the WolframAlpha client with the provided API key
app_id = 'XU774R-P2A5KVLWKP'
client = wolframalpha.Client(app_id)

# Blockchain Classes
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data  # This will store the transaction details (e.g., name, course, NFT path)
        self.hash = hash

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(0, "0", time(), "Genesis Block", self.hash_block("0", time(), "Genesis Block"))
        self.chain.append(genesis_block)

    def hash_block(self, previous_hash, timestamp, data):
        """Hash a block."""
        block_string = f"{previous_hash}{timestamp}{data}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_block(self, data):
        """Add a new block to the chain."""
        previous_block = self.chain[-1]
        index = len(self.chain)
        timestamp = time()
        hash = self.hash_block(previous_block.hash, timestamp, data)
        new_block = Block(index, previous_block.hash, timestamp, data, hash)
        self.chain.append(new_block)

    def get_chain(self):
        """Return the full blockchain."""
        return [block.to_dict() for block in self.chain]

    def get_last_block(self):
        """Return the last block in the chain."""
        return self.chain[-1] if self.chain else None

# Simulate a basic education platform with 2 courses and a quiz
courses = {
    "Blockchain 101": [
        {"question": "What is a blockchain?", "options": ["A database", "A chain of blocks", "A programming language"], "answer": "A chain of blocks"},
        {"question": "Which technology is behind Bitcoin?", "options": ["Blockchain", "Ethereum", "Ripple"], "answer": "Blockchain"}
    ],
    "Cryptocurrency Basics": [
        {"question": "What is Bitcoin?", "options": ["A cryptocurrency", "A digital wallet", "A bank"], "answer": "A cryptocurrency"},
        {"question": "Which algorithm does Bitcoin use?", "options": ["PoW", "PoS", "DPoS"], "answer": "PoW"}
    ]
}

# Initialize blockchain
blockchain = Blockchain()

def generate_nft(name):
    """Generate a simple NFT-like image with the user's name."""
    img = Image.new('RGB', (300, 150), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    text = f"{name}'s NFT"
    d.text((10, 10), text, fill=(255, 255, 0))

    # Save it as a file
    nft_path = f"nft_{name}.png"
    img.save(nft_path)
    return nft_path

def get_wolfram_response(query):
    """Send query to WolframAlpha and return the response."""
    try:
        result = client.query(query)
        answer = next(result.results).text
        return answer
    except Exception as e:
        return "Sorry, I couldn't find an answer for that."

def display_course(courses, name):
    """Display available courses and allow the user to select one."""
    st.write("### Available Courses")
    course_choice = st.selectbox("Select a course", list(courses.keys()))
    
    st.write(f"### {course_choice} Quiz")
    quiz = courses[course_choice]
    
    score = 0
    for question in quiz:
        st.write(question["question"])
        user_answer = st.radio("Your answer", question["options"])
        if user_answer == question["answer"]:
            score += 1
    
    if score == len(quiz):
        st.success("You passed the quiz! Generating NFT...")

        # Generate NFT
        nft_image = generate_nft(name)
        st.image(nft_image)

        # Save NFT info to blockchain
        transaction_data = {
            "name": name,
            "course": course_choice,
            "nft_image": nft_image
        }
        blockchain.add_block(transaction_data)

        # Display blockchain
        st.write("### Blockchain:")
        st.json(blockchain.get_chain())

        # Provide download for the NFT
        with open(nft_image, "rb") as file:
            st.download_button("Download your NFT", file, file_name=nft_image)
        os.remove(nft_image)  # Clean up the generated file
    else:
        st.warning("You did not pass the quiz. Try again!")

# Main Streamlit app
def main():
    st.title("Blockchain Education Platform")

    # Step 1: Get user name
    name = st.text_input("Enter your name")
    if name:
        st.write(f"Hello, {name}! Let's get started.")
        display_course(courses, name)  # Pass name to display_course function
    else:
        st.write("Please enter your name to proceed.")
    
    # Add a chat-like widget for WolframAlpha
    st.sidebar.title("Ask WolframAlpha")
    user_query = st.sidebar.text_input("Ask something (e.g., 'What is blockchain?'):")

    if user_query:
        answer = get_wolfram_response(user_query)
        st.sidebar.write(f"Answer from WolframAlpha: {answer}")

if __name__ == "__main__":
    main()
