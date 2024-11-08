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

theLibrary = {}

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

def addBook(author, title, isbn, edition, amount):
    responses = []
    if isbn in theLibrary:
        theLibrary['numAvailable'] += amount
    else:
        theLibrary[isbn] = {
            "title": title,
            "author": author,
            "numAvailable": amount,
            "numUnavailable": 0,
            "edition": edition
        }
    responses.append('Added new book {0}'.format(isbn))
    return responses

def removeBook(isbn, amount):
    responses = []
    if isbn in theLibrary:
        if amount <= theLibrary[isbn]['numAvailable']:
            theLibrary[isbn]['numAvailable'] -= amount
            responses.append('Removed {0} of book {1}'.format(amount, isbn))
        else:
            responses.append('WARNING: Not enough books of {0} to remove'.format(isbn))
    else:
        responses.append('WARNING: Book {0} not found'.format(isbn))
    return responses

def borrowBook(isbn, amount):
    responses = []
    if isbn in theLibrary:
        if amount <= theLibrary[isbn]['numAvailable']:
            theLibrary[isbn]['numAvailable'] -= amount
            theLibrary[isbn]['numUnavailable'] += amount
            responses.append('{0} of book {1} borrowed'.format(amount, isbn))
        else:
            responses.append('WARNING: No available books')
    else:
        responses.append("WARNING: No books found")
    return responses

def returnBook(isbn, amount):
    responses = []
    if isbn in theLibrary:
        if amount <= theLibrary[isbn]['numUnavailable']:
            theLibrary[isbn]['numUnavailable'] -= amount
            theLibrary[isbn]['numAvailable'] += amount
            responses.append('{0} of book {1} returned'.format(amount, isbn))
        else:
            responses.append('WARNING: Books already available')
    else:
        responses.append("WARNING: No books found")
    return responses

def searchBook(title, author):
    responses = []
    foundBooks = []
    for isbn in theLibrary:
        book = theLibrary[isbn]
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
        responses.append("WARNING: No books found")
    else:
        responses = foundBooks
    return responses

def searchBookTitle(title):
    responses = []
    foundBooks = []
    for isbn in theLibrary:
        book = theLibrary[isbn]
        bookTitle = book['title']
        numAvail = book["numAvailable"]

        if title.lower() in bookTitle.lower() and numAvail > 0:
            author = book['author']
            edition = book['edition']
            bookAvailable = "{0}, {1}, Available, {2}, {3}".format(bookTitle, author, isbn, edition)
            books = [bookAvailable] * numAvail
            foundBooks += books
    if not foundBooks:
        responses.append("WARNING: No books found")
    else:
        responses = foundBooks
    return responses

def searchBookAuthor(author):
    responses = []
    foundBooks = []
    for isbn in theLibrary:
        book = theLibrary[isbn]
        bookAuthor = book['author']
        numAvail = book['numAvailable']

        if author.lower() == bookAuthor.lower() and numAvail > 0:
            title = book['title']
            edition = book['edition']
            bookAvailable = "{0}, {1}, Available, {2}, {3}".format(title, bookAuthor, isbn, edition)
            books = [bookAvailable] * numAvail
            foundBooks += books
    if not foundBooks:
        responses.append("WARNING: No books found")
    else:
        responses = foundBooks
    return responses

def searchBookISBN(isbn):
    responses = []
    foundBooks = []
    if isbn in theLibrary:
        book = theLibrary[isbn]
        title = book['title']
        author = book['author']
        edition = book['edition']
        numAvail = book['numAvailable']
        bookAvailable = "{0}, {1}, Available, {2}, {3}".format(title, author, isbn, edition)
        books = [bookAvailable] * numAvail
        foundBooks += books
    if not foundBooks:
        responses.append("WARNING: No books found")
    else:
        responses = foundBooks
    return responses

def listAvailableBooks():
    responses = []
    availableBooks = []
    for isbn in theLibrary:
        book = theLibrary[isbn]
        numAvail = book['numAvailable']
        if numAvail > 0:
            title = book['title']
            author = book['author']
            edition = book['edition']
            bookAvailable = "{0}, {1}, Available, {2}, {3}".format(title, author, isbn, edition)
            books = [bookAvailable] * numAvail
            availableBooks += books
    if not availableBooks:
        responses.append("WARNING: No books found")
    else:
        responses = availableBooks
    return responses

def listAvailableAuthors():
    responses = []
    availableAuthors = set()
    for isbn in theLibrary:
        book = theLibrary[isbn]
        numAvail = book['numAvailable']
        if numAvail > 0:
            availableAuthors.add(book['author'])
    if not availableAuthors:
        responses.append("WARNING: No available authors found")
    else:
        responses = list(availableAuthors)
    return responses

def processCommands(inputFile):
    with open(inputFile, 'r') as file:
        for line in file:
            command = line.strip()
            responses = runCommand(command)
            for response in responses:
                print(response)

def runCommand(inputCommand):
    responses = []
    command, *options = inputCommand.split('*')
    if command == 'AddBook':
        responses = addBook(options[0], options[1], options[2], options[3], options[4])
    elif command == 'RemoveBook':
        responses = removeBook(options[0], options[1])
    elif command == 'BorrowBook':
        responses = borrowBook(options[0], options[1])
    elif command == 'ReturnBook':
        responses = returnBook(options[0], options[1])
    elif command == 'SearchBook':
        responses = searchBook(options[0], options[1])
    elif command == 'SearchBookTitle':
        responses = searchBookTitle(options[0])
    elif command == 'SearchBookAuthor':
        responses = searchBookAuthor(options[0])
    elif command == 'SearchBookISBN':
        responses = searchBookISBN(options[0])
    elif command == 'ListAvailableBooks':
        responses = listAvailableBooks()
    elif command == 'ListAvailableAuthors':
        responses = listAvailableAuthors()
    return responses
