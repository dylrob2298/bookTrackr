import pytest
from library import Library, runCommand

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
    assert "WARNING: Book not found" in response

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
