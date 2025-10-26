import faiss
import numpy as np
import requests
import json
import pickle
import os
import uuid

class VectorDBManager:
    """
    A manager class to handle interactions with a FAISS vector database.
    This class uses Ollama for embedding generation and supports metadata filters.
    
    Prerequisites:
    - An Ollama instance must be running.
    - An embedding model (e.g., 'nomic-embed-text') must be pulled in Ollama.
      Run `ollama pull nomic-embed-text` in your terminal.
    """
    def __init__(self, path: str = "./faiss_db", ollama_model: str = 'nomic-embed-text', ollama_base_url: str = 'http://localhost:11434'):
        """
        Initializes the VectorDBManager with FAISS and Ollama.

        Args:
            path (str): The directory path to store the persistent database files.
            ollama_model (str): The name of the embedding model to use in Ollama.
            ollama_base_url (str): The base URL for the Ollama API.
        """
        self.db_path = path
        self.index_file = os.path.join(path, "faiss.index")
        self.metadata_file = os.path.join(path, "metadata.pkl")
        
        # 1. Configure Ollama settings
        self.ollama_model = ollama_model
        self.ollama_api_url = f"{ollama_base_url}/api/embeddings"
        
        # The embedding dimension depends on the Ollama model.
        # 'mxbai-embed-large' has a dimension of 1024.
        # 'nomic-embed-text' has a dimension of 768.
        # Adjust this if you use a different model.
        self.embedding_dim = 768 

        # Create the directory if it doesn't exist
        os.makedirs(self.db_path, exist_ok=True)

        # 2. Load the FAISS index and metadata if they exist, otherwise initialize them
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            print(f"Loading existing FAISS index from {self.index_file}")
            self.index = faiss.read_index(self.index_file)
            with open(self.metadata_file, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            print("Initializing new FAISS index and metadata.")
            # Use IndexFlatL2 for simple L2 distance search
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.metadata = {}

    def _get_ollama_embedding(self, text: str) -> np.ndarray:
        """Generates an embedding for the given text using the Ollama API."""
        try:
            payload = {
                "model": self.ollama_model,
                "prompt": text
            }
            response = requests.post(self.ollama_api_url, json=payload)
            response.raise_for_status() # Raise an exception for bad status codes
            
            embedding = response.json().get("embedding")
            if not embedding:
                raise ValueError("Ollama API response did not contain an embedding.")
            
            return [embedding] # Return as a list of lists for consistency
        
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            print(f"Please ensure Ollama is running and the model '{self.ollama_model}' is available.")
            return None
        except ValueError as e:
            print(f"Error processing Ollama response: {e}")
            return None

    def save(self):
        """Saves the FAISS index and metadata to disk."""
        print(f"Saving FAISS index to {self.index_file}")
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, 'wb') as f:
            pickle.dump(self.metadata, f)
        print("Save complete.")

    def add_lesson_content(self, content: str, lesson_number: int, source_notebook: str):
        """
        Adds a piece of lesson content to the vector database.

        Args:
            content (str): The text content from the lesson.
            lesson_number (int): The lesson number this content belongs to.
            source_notebook (str): The filename of the notebook this content came from.
        """
        # Create the vector embedding for the content using Ollama
        vector = self._get_ollama_embedding(content)
        if vector is None:
            return # Don't add if embedding failed

        # Add the vector to the FAISS index
        self.index.add(np.array(vector, dtype=np.float32))
        
        # Store the corresponding metadata.
        index_position = self.index.ntotal - 1
        self.metadata[index_position] = {
            "content": content,
            "lesson_number": lesson_number,
            "source": source_notebook
        }
        print(f"Added content from '{source_notebook}' (Lesson {lesson_number}).")

    def clear_all(self):
        """Clears the entire FAISS index and metadata."""
        self.index.reset()
        self.metadata = {}
        print("Cleared all data from the vector database.")

    def search_with_filter(self, query: str, max_lesson_number: int, num_results: int = 2):
        """
        Searches the database for content relevant to a query using metadata filtering.

        Args:
            query (str): The user's question or search term.
            max_lesson_number (int): The maximum lesson number to include in the search.
            num_results (int): The number of relevant documents to return.

        Returns:
            list: A list of the most relevant document contents.
        """
        if self.index.ntotal == 0:
            return []

        # Create embedding for the query using Ollama
        query_vector = self._get_ollama_embedding(query)
        if query_vector is None:
            return []

        # Search the index for more results than we need, to allow for filtering
        search_k = max(10, num_results * 5)
        distances, indices = self.index.search(np.array(query_vector, dtype=np.float32), k=min(search_k, self.index.ntotal))

        # Filter the results based on metadata
        filtered_results = []
        for i in indices[0]:
            if i in self.metadata and self.metadata[i]["lesson_number"] <= max_lesson_number:
                filtered_results.append(self.metadata[i]["content"])
            if len(filtered_results) >= num_results:
                break
        
        return filtered_results

# --- Example Usage ---
if __name__ == "__main__":
    db_path = "./faiss_db_test_ollama"
    # Clean up previous runs for a fresh start
    if os.path.exists(db_path):
        import shutil
        shutil.rmtree(db_path)
        
    # 1. Initialize the manager. This will create a 'faiss_db_test_ollama' folder.
    db_manager = VectorDBManager(path=db_path)
    
    # 2. Add content for Lesson 1 & 2
    db_manager.add_lesson_content(
        "A qubit is the basic unit of quantum information. Unlike a classical bit, a qubit can be in a superposition of both 0 and 1 at the same time.",
        lesson_number=1,
        source_notebook="01-Qubits.ipynb"
    )
    db_manager.add_lesson_content(
        "The Hadamard gate is a fundamental quantum gate. It takes a qubit in state |0> and puts it into an equal superposition state, |+>.",
        lesson_number=2,
        source_notebook="02-Gates.ipynb"
    )
    
    # 3. Save the database to disk
    db_manager.save()

    print("\n" + "="*20 + "\n")

    # 4. Simulate a search for a student who has only completed Lesson 1
    print("Searching for a student on Lesson 1 who asks about the 'Hadamard gate':")
    student_query = "What is the Hadamard gate?"
    student_progress = 1
    search_results = db_manager.search_with_filter(student_query, student_progress)
    
    if search_results:
        print("Found results:")
        for result in search_results:
            print(f"- {result}")
    else:
        print("Found NO results. The student hasn't learned about this yet!")
        
    print("\n" + "="*20 + "\n")

    # 5. Simulate a search for a student who has completed Lesson 2
    print("Searching for a student on Lesson 2 who asks about the 'Hadamard gate':")
    student_progress = 2
    search_results = db_manager.search_with_filter(student_query, student_progress)

    if search_results:
        print("Found results:")
        for result in search_results:
            print(f"- {result}")
    else:
        print("Found NO results.")

    # cleanup after test
    if os.path.exists(db_path):
        import shutil
        shutil.rmtree(db_path)

