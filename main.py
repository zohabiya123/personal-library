import streamlit as st  # type: ignore
import json
import time

st.set_page_config(page_title="Personal Library", page_icon=":books:", layout="wide")

st.title("📚 Personal Library")

st.markdown("""
    <style>
    div.stButton > button{
        background-color: #ff6347;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        padding: 12px 24px;
        transition: 0.3s;
    }
    div.stButton > button:hover{
        background-color: #ff4500;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Load and save library functions
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library(library):
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)

library = load_library()

# Sidebar options
choice = st.sidebar.radio("📌 Choose an option:", ["Add Book", "Remove Book", "Display Books", "Search Books", "Display Statistics"])

# Function to add a book
def add_book():
    title = st.text_input("📖 Enter the title of the book:")
    author = st.text_input("✍️ Enter the author of the book:")
    publication_year = st.number_input("📅 Enter the publication year of the book:", min_value=1000, max_value=2025, value=2024)
    genre = st.text_input("🎭 Enter the genre of the book:")
    read_status = st.selectbox("📌 Read status:", ["Not Read", "Read"])
    
    if st.button("✅ Add Book"):
        if title and author and publication_year and genre and read_status:
            item = {
                "title": title,
                "author": author,
                "publication year": publication_year,
                "genre": genre,
                "read status": read_status
            }
            library.append(item)
            save_library(library)
            st.success(f"📚 Book '{title}' added successfully!")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("⚠️ Please fill all the fields!")

# Remove book
def remove_book():
    st.subheader("🗑️ Remove a book")
    book_titles = [book["title"] for book in library]
    if book_titles:
        selected_title = st.selectbox("📌 Select a book to remove:", book_titles)
        if st.button("🗑️ Remove Book"):
            library[:] = [book for book in library if book["title"] != selected_title]
            save_library(library)
            st.success(f"📖 Book '{selected_title}' removed successfully!")
            time.sleep(1.5)
            st.rerun()
    else:
        st.warning("⚠️ No books in the library!")

# Search books
def search_books():
    st.subheader("🔎 Search Books")
    search = st.text_input("🔍 Enter book title or author:")
    if st.button("🔎 Search"):
        results = [book for book in library if search.lower() in book["title"].lower() or search.lower() in book["author"].lower()]
        if results:
            st.table(results)
        else:
            st.warning("⚠️ No books found!")

# Display books
def display_books():
    st.subheader("📚 All Books")
    if library:
        st.table(library)
    else:
        st.warning("⚠️ No books in the library!")

# Display statistics
def display_statistics():
    st.subheader("📊 Library Statistics")
    if library:
        total_books = len(library)
        read_books = sum(1 for book in library if book["read status"] == "Read")
        not_read_books = total_books - read_books
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="📚 Total Books", value=total_books)
        with col2:
            st.metric(label="✅ Read Books", value=read_books)
        with col3:
            st.metric(label="📖 Not Read Books", value=not_read_books)
    else:
        st.warning("⚠️ No books in the library!")

# Execute functions based on user choice
if choice == "Add Book":
    add_book()
elif choice == "Remove Book":
    remove_book()
elif choice == "Search Books":
    search_books()
elif choice == "Display Books":
    display_books()
elif choice == "Display Statistics":
    display_statistics()