"""Library management system, a database of books
each Book, in  Library.txt:
- Title (string)
- Author (string)
- Availability (string that is "true" or "false")
- ISBN (string)
- Edition (string)

Representation we will use after reading Library.txt
Book (ISBN as key in dict):
- title (string)
- author (string)
- numAvailable (int)
- numUnavailable (int)
- edition (string)
"""

def readLibrary(libraryFile):
    library = {}
    with open(libraryFile, 'r') as file:
        for line in file:
            bookTitle, bookAuthor, availability, isbn, edition = line.strip().split(',')
            bookIsAvailable = availability == "true"
            if isbn in library:
                if bookIsAvailable:
                    library[isbn]["numAvailable"] += 1
                else:
                    library[isbn]["numUnavailable"] += 1
            else:
                library[isbn] = {
                    "title": bookTitle,
                    "author": bookAuthor,
                    "numAvailable": 1 if bookIsAvailable else 0,
                    "numUnavailable": 0 if bookIsAvailable else 1,
                    "edition": edition
                }
    return library

def updateLibrary(library):
    libraryFile = "Library.txt"
    with open(libraryFile, 'w') as file:
        # key is the isbn
        for key in library:
            book = library[key]
            title = book["title"]
            author = book["author"]
            edition = book["edition"]
            numAvail = book["numAvailable"]
            numUnavail = book["numUnavailable"]
            bookAvailable = "{0},{1},true,{2},{3}\n".format(title, author, key, edition)
            bookUnavailable = "{0},{1},false,{2},{3}\n".format(title, author, key, edition)
            books = [bookAvailable] * numAvail + [bookUnavailable] * numUnavail
            file.writelines(books)

def addBook(library, author, title, isbn, edition, amount):
    if isbn in library:
        library['numAvailable'] += amount
    else:
        library[isbn] = {
            "title": title,
            "author": author,
            "numAvailable": amount,
            "numUnavailable": 0,
            "edition": edition
        }
    return library

def removeBook(library, isbn, amount):
    if isbn in library:
        if amount <= library[isbn]['numAvailable']:
            library[isbn]['numAvailable'] -= amount
        # else: print not enough books
    # else: print book not found
    return library

def borrowBook(library, isbn, amount):
    if isbn in library:
        if amount <= library[isbn]['numAvailable']:
            library[isbn]['numAvailable'] -= amount
            library[isbn]['numUnavailable'] += amount
        # else: print not enough available books
    # else: print book not found
    return library

def returnBook(library, isbn, amount):
    if isbn in library:
        if amount <= library[isbn]['numUnavailable']:
            library[isbn]['numUnavailable'] -= amount
            library[isbn]['numAvailable'] += amount
        # else: print books already available
    # else: print book not found
    return library

def searchBook(library, title, author):
    foundBooks = []
    for isbn in library:
        book = library[isbn]
        bookTitle = book['title']
        bookAuthor = book['author']
        if title.lower() == bookTitle.lower() and author.lower() == bookAuthor.lower():
            edition = book["edition"]
            numAvail = book["numAvailable"]
            numUnavail = book["numUnavailable"]
            bookAvailable = "{0}, {1}, Available, {2}, {3}".format(bookTitle, bookAuthor, isbn, edition)
            bookUnavailable = "{0}, {1}, Unavailable, {2}, {3}".format(bookTitle, bookAuthor, isbn, edition)
            books = [bookAvailable] * numAvail + [bookUnavailable] * numUnavail
            foundBooks += books
    if not foundBooks:
        print("book not found")
        return False
    for book in foundBooks:
        print(book)
    return True

def searchBookTitle(library, title):
    foundBooks = []
    for isbn in library:
        book = library[isbn]
        bookTitle = book['title']
        numAvail = book["numAvailable"]

        if title.lower() in bookTitle.lower() and numAvail > 0:
            author = book['author']
            edition = book['edition']
            bookAvailable = "{0}, {1}, Available, {2}, {3}".format(bookTitle, author, isbn, edition)
            books = [bookAvailable] * numAvail
            foundBooks += books
    if not foundBooks:
        print("book not found")
        return False
    for book in foundBooks:
        print(book)
    return True

def searchBookAuthor(library, author):
    foundBooks = []
    for isbn in library:
        book = library[isbn]
        bookAuthor = book['author']
        numAvail = book['numAvailable']

        if author.lower() == bookAuthor.lower() and numAvail > 0:
            title = book['title']
            edition = book['edition']
            bookAvailable = "{0}, {1}, Available, {2}, {3}".format(title, bookAuthor, isbn, edition)
            books = [bookAvailable] * numAvail
            foundBooks += books
    if not foundBooks:
        print("no books by author")
        return False
    for book in foundBooks:
        print(book)
    return True

