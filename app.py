import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
DATA_FILE = 'books.json'

# --- Utility Functions for JSON Saving/Loading ---

def load_books():
    """Reads the book data from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            # Handle empty file case
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        return []
    except json.JSONDecodeError:
        # Handle invalid JSON format
        print(f"Error decoding JSON from {DATA_FILE}. Starting with an empty list.")
        return []

def save_books(books):
    """Writes the book data back to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        # Use indent for readability in the file
        json.dump(books, f, indent=4)

# --- Flask Routes (The "API" Endpoints) ---

# Renders the main dashboard page (GET /)
@app.route('/')
def index():
    books = load_books()
    # Pass the list of books to the HTML template
    return render_template('index.html', books=books)

# API to add a new book (POST /api/books)
@app.route('/api/books', methods=['POST'])
def add_book():
    books = load_books()
    
    # Get the data from the form submission
    data = request.form
    
    # Determine the next available ID
    new_id = max([book['id'] for book in books]) + 1 if books else 1
    
    new_book = {
        'id': new_id,
        'title': data.get('title'),
        'author': data.get('author'),
        # Convert checkbox value to a boolean
        'completed': 'completed' in data,
        'rating': int(data.get('rating', 0)) # Ensure rating is an integer
    }

    books.append(new_book)
    save_books(books)
    
    # Redirect back to the main page after adding the book
    return redirect(url_for('index'))

# API to delete a book (POST /api/books/delete/<int:book_id>)
@app.route('/api/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    books = load_books()
    # Filter out the book with the matching ID
    books = [book for book in books if book['id'] != book_id]
    
    save_books(books)
    
    # Redirect back to the main page
    return redirect(url_for('index'))

# API to get all books (GET /api/books) - Simple API endpoint example
@app.route('/api/books', methods=['GET'])
def get_all_books():
    books = load_books()
    # Return JSON data for use by other apps or JavaScript
    return jsonify(books)

# --- Run the App ---
if __name__ == '__main__':
    # When you're ready to deploy, set debug=False
    app.run(debug=True)