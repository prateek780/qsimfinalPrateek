import os
import json
import re
try: 
    from .vector_db_manager import VectorDBManager
except ImportError:
    from dev.v_db.vector_db_manager import VectorDBManager
import shutil

def extract_content_chunks_from_notebook(notebook_path):
    """
    Parses a Jupyter Notebook file and extracts the content from all markdown
    cells as a list of individual chunks.

    Args:
        notebook_path (str): The full path to the .ipynb file.

    Returns:
        list[str]: A list of strings, where each string is the content of one markdown cell.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        markdown_chunks = []
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                # The 'source' is a list of strings (lines), join them into a single string for the cell.
                # Add this complete cell content as one chunk.
                cell_content = "".join(cell.get('source', []))
                if cell_content.strip(): # Ensure the cell is not empty
                    markdown_chunks.append(cell_content)
        
        return markdown_chunks

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading or parsing notebook {notebook_path}: {e}")
        return []

def index_course_content(root_folder: str, db_manager: VectorDBManager):
    """
    Recursively scans a folder for .ipynb files, extracts their content,
    and adds it to the vector database.

    Args:
        root_folder (str): The path to the root folder of the course content.
        db_manager (VectorDBManager): An instance of the VectorDBManager.
    """
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Exclude '.ipynb_checkpoints' folders from the search
        if '.ipynb_checkpoints' in dirnames:
            dirnames.remove('.ipynb_checkpoints')

        for filename in sorted(filenames): # Sort to process in a predictable order
            if filename.endswith(".ipynb"):
                # Try to infer lesson number from the start of the filename (e.g., "01-...")
                match = re.match(r'^(\d+)', filename)
                if match:
                    lesson_number = int(match.group(1))
                else:
                    print(f"Warning: Could not infer lesson number for '{filename}'. Skipping.")
                    continue

                full_path = os.path.join(dirpath, filename)
                print(f"Processing: {full_path} as Lesson {lesson_number}")

                content_chunks = extract_content_chunks_from_notebook(full_path)

                if content_chunks:
                    print(f"  Found {len(content_chunks)} markdown chunks to index.")
                    for chunk in content_chunks:
                        db_manager.add_lesson_content(
                            content=chunk,
                            lesson_number=lesson_number,
                            source_notebook=filename
                        )

# --- Example Usage ---
if __name__ == "__main__":
    # --- 1. Setup a dummy course structure for demonstration ---
    COURSE_DIR = "./course_content"
    DB_PATH = "./faiss_course_db"

    # Clean up previous runs
    if os.path.exists(COURSE_DIR):
        shutil.rmtree(COURSE_DIR)
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    os.makedirs(os.path.join(COURSE_DIR, "module1"))
    os.makedirs(os.path.join(COURSE_DIR, "module2/.ipynb_checkpoints")) # a folder to ignore

    # Create dummy notebook 1
    notebook1_content = {
        "cells": [
            {"cell_type": "markdown", "source": ["# Lesson 1: The Qubit\n", "A qubit is the basic unit of quantum information."]},
            {"cell_type": "code", "source": ["print('Hello Qubit!')"]}
        ], "metadata": {}, "nbformat": 4, "nbformat_minor": 2
    }
    with open(os.path.join(COURSE_DIR, "module1/01-qubits.ipynb"), 'w') as f:
        json.dump(notebook1_content, f)

    # Create dummy notebook 2
    notebook2_content = {
        "cells": [
            {"cell_type": "markdown", "source": ["# Lesson 2: Superposition\n", "The Hadamard gate creates superposition."]}
        ], "metadata": {}, "nbformat": 4, "nbformat_minor": 2
    }
    with open(os.path.join(COURSE_DIR, "module2/02-superposition.ipynb"), 'w') as f:
        json.dump(notebook2_content, f)
        
    print("Created dummy course structure for testing.")
    print("-" * 30)

    # --- 2. Initialize the DB Manager and run the indexing ---
    db_manager = VectorDBManager(path=DB_PATH)
    
    print("Starting to index course content...")
    index_course_content(COURSE_DIR, db_manager)
    
    # --- 3. Save the newly populated database ---
    db_manager.save()
    print("-" * 30)

    # --- 4. Verify the indexing with a search ---
    print("Verifying search for a student on Lesson 1:")
    results = db_manager.search_with_filter("What is a qubit?", max_lesson_number=1)
    print(f"Search Results: {results}")

    print("\nVerifying search for a student on Lesson 2:")
    results = db_manager.search_with_filter("What is superposition?", max_lesson_number=2)
    print(f"Search Results: {results}")

    # Clean up dummy files
    shutil.rmtree(COURSE_DIR)
    shutil.rmtree(DB_PATH)
    print("\nCleaned up dummy files.")
