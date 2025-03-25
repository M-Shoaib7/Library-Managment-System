import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# Initialize session state for the library if it doesn't exist
if 'library' not in st.session_state:
    st.session_state.library = []

# File handling functions
def save_library_to_file(filename="library.json"):
    """Save the library to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(st.session_state.library, f)
        st.success(f"Library saved successfully to {filename}!")
    except Exception as e:
        st.error(f"Error saving library: {e}")

def load_library_from_file(filename="library.json"):
    """Load the library from a JSON file"""
    try:
        if Path(filename).exists():
            with open(filename, 'r') as f:
                st.session_state.library = json.load(f)
            st.success(f"Library loaded successfully from {filename}!")
        else:
            st.warning(f"No saved library found at {filename}")
    except Exception as e:
        st.error(f"Error loading library: {e}")

# Book management functions
def add_book(title, author, year, genre, read_status):
    """Add a new book to the library"""
    new_book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read_status": read_status,
        "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(new_book)
    st.success(f"Book '{title}' added successfully!")

def remove_book(title):
    """Remove a book from the library by title"""
    removed = False
    for i, book in enumerate(st.session_state.library):
        if book['title'].lower() == title.lower():
            st.session_state.library.pop(i)
            removed = True
            break
    
    if removed:
        st.success(f"Book '{title}' removed successfully!")
    else:
        st.warning(f"Book '{title}' not found in the library.")

def search_books(search_term, search_by="title"):
    """Search for books by title, author, or genre"""
    results = []
    for book in st.session_state.library:
        if search_term.lower() in book[search_by].lower():
            results.append(book)
    return results

def calculate_statistics():
    """Calculate library statistics"""
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read_status'])
    
    stats = {
        "total_books": total_books,
        "read_books": read_books,
        "unread_books": total_books - read_books,
        "read_percentage": (read_books / total_books * 100) if total_books > 0 else 0
    }
    return stats

# Streamlit UI
st.title("📚 Personal Library Manager")

# Menu system
menu_options = [
    "Add a Book",
    "Remove a Book",
    "Search for Books",
    "View All Books",
    "View Statistics",
    "Save/Load Library"
]
choice = st.sidebar.selectbox("Menu", menu_options)

if choice == "Add a Book":
    st.header("Add a New Book")
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        title = col1.text_input("Title*", placeholder="Book title")
        author = col2.text_input("Author*", placeholder="Book author")
        year = col1.number_input("Publication Year*", min_value=0, max_value=datetime.now().year)
        genre = col2.selectbox("Genre*", [
            "Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
            "Mystery", "Thriller", "Romance", "Biography", 
            "History", "Self-Help", "Psychology" , "Computer Science", "Data Science", "Machine Learning", "Deep Learning", "Artificial Intelligence", "Business", "Economics", "Finance", "Marketing", "Management", "Other"
        ])
        read_status = st.checkbox("I have read this book")
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if title and author and year:
                add_book(title, author, year, genre, read_status)
            else:
                st.warning("Please fill in all required fields (marked with *)")

elif choice == "Remove a Book":
    st.header("Remove a Book")
    if st.session_state.library:
        book_titles = [book['title'] for book in st.session_state.library]
        title_to_remove = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            remove_book(title_to_remove)
    else:
        st.info("Your library is empty. Add some books first!")

elif choice == "Search for Books":
    st.header("Search for Books")
    search_by = st.radio("Search by:", ["title", "author", "genre"])
    search_term = st.text_input(f"Enter {search_by} to search")
    
    if search_term:
        results = search_books(search_term, search_by)
        if results:
            st.subheader(f"Found {len(results)} book(s):")
            for book in results:
                st.write(f"**{book['title']}** by {book['author']} ({book['year']})")
                st.write(f"Genre: {book['genre']} | Read: {'✅' if book['read_status'] else '❌'}")
                st.write("---")
        else:
            st.warning("No books found matching your search.")

elif choice == "View All Books":
    st.header("Your Library")
    if st.session_state.library:
        st.write(f"Total books: {len(st.session_state.library)}")
        
        # Sort options
        sort_by = st.selectbox("Sort by", ["Recently Added", "Title", "Author", "Year"])
        reverse_sort = st.checkbox("Reverse order")
        
        # Create a sorted copy of the library
        sorted_library = st.session_state.library.copy()
        
        if sort_by == "Recently Added":
            sorted_library.sort(key=lambda x: x['added_date'], reverse=not reverse_sort)
        elif sort_by == "Title":
            sorted_library.sort(key=lambda x: x['title'].lower(), reverse=reverse_sort)
        elif sort_by == "Author":
            sorted_library.sort(key=lambda x: x['author'].lower(), reverse=reverse_sort)
        elif sort_by == "Year":
            sorted_library.sort(key=lambda x: x['year'], reverse=reverse_sort)
        
        for book in sorted_library:
            # Create expandable sections for each book
            with st.expander(f"{book['title']} by {book['author']}"):
                col1, col2 = st.columns([3, 1])
                col1.write(f"**Author:** {book['author']}")
                col1.write(f"**Year:** {book['year']}")
                col1.write(f"**Genre:** {book['genre']}")
                col2.write(f"**Read:** {'Yes' if book['read_status'] else 'No'}")
                col2.write(f"**Added:** {book['added_date']}")
    else:
        st.info("Your library is empty. Add some books first!")

elif choice == "View Statistics":
    st.header("Library Statistics")
    if st.session_state.library:
        stats = calculate_statistics()
        
        st.metric("Total Books", stats['total_books'])
        st.metric("Books Read", f"{stats['read_books']} ({stats['read_percentage']:.1f}%)")
        st.metric("Books Unread", stats['unread_books'])
        
        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart({
                "Read": [stats['read_books']],
                "Unread": [stats['unread_books']]
            })
        with col2:
            st.write("Read Status Distribution")
            st.progress(stats['read_percentage'] / 100)
    else:
        st.info("Your library is empty. Add some books first to see statistics!")

elif choice == "Save/Load Library":
    st.header("Save or Load Your Library")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Save Library")
        save_filename = st.text_input("Save filename", "library.json")
        if st.button("Save Library"):
            save_library_to_file(save_filename)
    
    with col2:
        st.subheader("Load Library")
        load_filename = st.text_input("Load filename", "library.json")
        if st.button("Load Library"):
            load_library_from_file(load_filename)
    
    st.warning("Note: Loading a library will replace your current library data.")