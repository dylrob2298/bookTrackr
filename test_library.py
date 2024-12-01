import pytest
from library import Library, runCommand, main

@pytest.fixture
def sample_library(tmp_path):
    # Create a sample Library.txt file with initial data
    library_file = tmp_path / "testLibrary.txt"
    library_file.write_text(
        "Around the World in Eighty Days,Jules Verne,true,9783401717005,1\n"
        "Around the World in Eighty Days,Jules Verne,false,9783401717005,1\n"
    )
    return Library(str(library_file))

def test_add_new_book_TC1(sample_library):
    response = runCommand(sample_library, "AddBook*H.G. Wells*The Time Machine*9780451530707*1*1")
    assert "Added new book 9780451530707" in response
    assert sample_library.books["9780451530707"]["numAvailable"] == 1

def test_add_existing_book_TC2(sample_library):
    response = runCommand(sample_library, "AddBook*Jules Verne*Around the World in Eighty Days*9783401717005*1*1")
    assert "Added new book 9783401717005" in response
    assert sample_library.books["9783401717005"]["numAvailable"] == 2

def test_remove_existing_book_TC3(sample_library):
    response = runCommand(sample_library, "RemoveBook*9783401717005*1")
    assert "Removed 1 of book 9783401717005" in response
    assert sample_library.books["9783401717005"]["numAvailable"] == 0

def test_remove_more_than_available_TC4(sample_library):
    response = runCommand(sample_library, "RemoveBook*9783401717005*50")
    assert "WARNING: Not enough books to remove" in response

def test_remove_nonexistent_book_TC5(sample_library):
    response = runCommand(sample_library, "RemoveBook*1111111111111*50")
    assert "WARNING: Book not found" in response

def test_borrow_valid_amount_TC6(sample_library):
    response = runCommand(sample_library, "BorrowBook*9783401717005*1")
    assert "1 of book 9783401717005 borrowed" in response
    assert sample_library.books["9783401717005"]["numAvailable"] == 0
    assert sample_library.books["9783401717005"]["numUnavailable"] == 2

def test_borrow_more_than_available_TC7(sample_library):
    response = runCommand(sample_library, "BorrowBook*9783401717005*50")
    assert "WARNING: No available books" in response

def test_borrow_nonexistent_book_TC8(sample_library):
    response = runCommand(sample_library, "BorrowBook*1111111111111*50")
    assert "WARNING: No books found" in response

def test_return_valid_amount_TC9(sample_library):
    runCommand(sample_library, "BorrowBook*9783401717005*1")
    response = runCommand(sample_library, "ReturnBook*9783401717005*1")
    assert "1 of book 9783401717005 returned" in response
    assert sample_library.books["9783401717005"]["numUnavailable"] == 1
    assert sample_library.books["9783401717005"]["numAvailable"] == 1

def test_return_more_than_unavailable_TC10(sample_library):
    response = runCommand(sample_library, "ReturnBook*9783401717005*50")
    assert "WARNING: Books already available" in response

def test_return_nonexistent_book_TC11(sample_library):
    response = runCommand(sample_library, "ReturnBook*1111111111111*50")
    assert "WARNING: No books found" in response

def test_search_book_TC12(sample_library):
    response = runCommand(sample_library, "SearchBook*Jules Verne*Around the World in Eighty Days")
    assert len(response) > 0
    assert "Around the World in Eighty Days" in response[0]

def test_search_nonexistent_book_TC13(sample_library):
    response = runCommand(sample_library, "SearchBook*Jules Verne*Journey to the Center of the Earth")
    assert "WARNING: No books found" in response

def test_search_book_title_TC14(sample_library):
    response = runCommand(sample_library, "SearchBookTitle*Eighty")
    assert len(response) > 0
    assert "Around the World in Eighty Days" in response[0]

def test_search_nonexistent_title_TC15(sample_library):
    response = runCommand(sample_library, "SearchBookTitle*Earth")
    assert "WARNING: No books found" in response

def test_search_book_author_TC16(sample_library):
    response = runCommand(sample_library, "SearchBookAuthor*Jules Verne")
    assert len(response) > 0
    assert "Jules Verne" in response[0]

def test_search_nonexistent_author_TC17(sample_library):
    response = runCommand(sample_library, "SearchBookAuthor*William Shakespeare")
    assert "WARNING: No books found" in response

def test_search_book_isbn_TC18(sample_library):
    response = runCommand(sample_library, "SearchBookISBN*9783401717005")
    assert len(response) > 0
    assert "9783401717005" in response[0]

def test_search_nonexistent_isbn_TC19(sample_library):
    response = runCommand(sample_library, "SearchBookISBN*1111111111111")
    assert "WARNING: No books found" in response

def test_list_available_books_TC20(sample_library):
    response = runCommand(sample_library, "ListAvailableBooks")
    assert len(response) > 0
    assert "Around the World in Eighty Days" in response[0]

def test_list_no_available_books_TC21(tmp_path):
    library_file = tmp_path / "EmptyLibrary.txt"
    library_file.write_text("")  # No books
    empty_library = Library(str(library_file))
    response = runCommand(empty_library, "ListAvailableBooks")
    assert "WARNING: No books found" in response

def test_list_available_authors_TC22(sample_library):
    response = runCommand(sample_library, "ListAvailableAuthors")
    assert len(response) > 0
    assert len(response) == 1
    assert "Jules Verne" in response

def test_list_no_available_authors_TC23(tmp_path):
    library_file = tmp_path / "EmptyLibrary.txt"
    library_file.write_text("")  # No books
    empty_library = Library(str(library_file))
    response = runCommand(empty_library, "ListAvailableAuthors")
    assert "WARNING: No available authors found" in response

# Added Tests for test cycle 2:

def test_main_TC24(tmp_path, monkeypatch):
    # Step 1: Create a temporary Library.txt (initial content for the mock)
    library_file = tmp_path / "Library.txt"
    library_file.write_text(
        "Book1,Author1,true,1234567890123,1\n"
        "Book2,Author2,true,9876543210987,2\n"
    )

    # Step 2: Create a temporary input.txt with a command to add a book
    input_file = tmp_path / "input.txt"
    input_file.write_text("AddBook*Book3*Author3*30*15\n")

    # Step 3: Mock the library's __init__ method to avoid file reading
    def mock_library_init(self, filepath):
        assert filepath.endswith("Library.txt")  # Ensure the correct file path
        self.libraryFile = str(library_file)  # Use the mocked file path
        self.books = {
            "1234567890123": {"title": "Book1", "author": "Author1", "edition": "1", "numAvailable": 1, "numUnavailable": 0},
            "9876543210987": {"title": "Book2", "author": "Author2", "edition": "2", "numAvailable": 2, "numUnavailable": 0},
        }

    # Step 4: Mock processCommands to simulate command processing without actually modifying the library
    def mock_process_commands(library, input_path):
        assert input_path.endswith("input.txt")  # Ensure correct input path is used
        library.addBook("Book3", "Author3", 1234567890348, 1, 1)

    # Use monkeypatch to replace the real methods with the mocks
    monkeypatch.setattr(Library, "__init__", mock_library_init)
    monkeypatch.setattr("library.processCommands", mock_process_commands)

    # Step 5: Run the main function
    main()  # We run the main function to trigger the file update

    # Step 6: Verify if the `updateLibrary` function updated the file correctly
    updated_content = library_file.read_text()  # Read the content of the Library.txt file

    # Check if the new book was added to the content
    assert "Author3,Book3,true,1234567890348,1" in updated_content
