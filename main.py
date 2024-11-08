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

# theLibrary = {}

class Library:
    def __init__(self, libraryFile):
        self.libraryFile = libraryFile
        self.books = self.readLibrary()

    def readLibrary(self):
        library = {}
        with open(self.libraryFile, 'r') as file:
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

    def updateLibrary(self):
        with open(self.libraryFile, 'w') as file:
            for isbn, book in self.books.items():
                title = book["title"]
                author = book["author"]
                edition = book["edition"]
                numAvail = book["numAvailable"]
                numUnavail = book["numUnavailable"]
                bookAvailable = f"{title},{author},true,{isbn},{edition}\n"
                bookUnavailable = f"{title},{author},false,{isbn},{edition}\n"
                books = [bookAvailable] * numAvail + [bookUnavailable] * numUnavail
                file.writelines(books)

    def addBook(self, author, title, isbn, edition, amount):
        responses = []
        amount = int(amount)
        if isbn in self.books:
            self.books['numAvailable'] += amount
        else:
            self.books[isbn] = {
                "title": title,
                "author": author,
                "numAvailable": amount,
                "numUnavailable": 0,
                "edition": edition
            }
        responses.append(f"Added new book {isbn}")
        return responses

    def removeBook(self, isbn, amount):
        responses = []
        amount = int(amount)
        if isbn in self.books:
            if amount <= self.books[isbn]['numAvailable']:
                self.books[isbn]['numAvailable'] -= amount
                responses.append(f'Removed {amount} of book {isbn}')
            else:
                responses.append('WARNING: Not enough books to remove')
        else:
            responses.append('WARNING: Book not found')
        return responses

    def borrowBook(self, isbn, amount):
        responses = []
        amount = int(amount)
        if isbn in self.books:
            if amount <= self.books[isbn]['numAvailable']:
                self.books[isbn]['numAvailable'] -= amount
                self.books[isbn]['numUnavailable'] += amount
                responses.append('{0} of book {1} borrowed'.format(amount, isbn))
            else:
                responses.append('WARNING: No available books')
        else:
            responses.append("WARNING: No books found")
        return responses

    def returnBook(self, isbn, amount):
        responses = []
        amount = int(amount)
        if isbn in self.books:
            if amount <= self.books[isbn]['numUnavailable']:
                self.books[isbn]['numUnavailable'] -= amount
                self.books[isbn]['numAvailable'] += amount
                responses.append('{0} of book {1} returned'.format(amount, isbn))
            else:
                responses.append('WARNING: Books already available')
        else:
            responses.append("WARNING: No books found")
        return responses

    def searchBook(self, title, author):
        responses = []
        foundBooks = []
        for isbn in self.books:
            book = self.books[isbn]
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

    def searchBookTitle(self, title):
        responses = []
        foundBooks = []
        for isbn in self.books:
            book = self.books[isbn]
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

    def searchBookAuthor(self, author):
        responses = []
        foundBooks = []
        for isbn in self.books:
            book = self.books[isbn]
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

    def searchBookISBN(self, isbn):
        responses = []
        foundBooks = []
        if isbn in self.books:
            book = self.books[isbn]
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

    def listAvailableBooks(self):
        responses = []
        availableBooks = []
        for isbn in self.books:
            book = self.books[isbn]
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

    def listAvailableAuthors(self):
        responses = []
        availableAuthors = set()
        for isbn in self.books:
            book = self.books[isbn]
            numAvail = book['numAvailable']
            if numAvail > 0:
                availableAuthors.add(book['author'])
        if not availableAuthors:
            responses.append("WARNING: No available authors found")
        else:
            responses = list(availableAuthors)
        return responses

def processCommands(library, inputFile):
    with open(inputFile, 'r') as file:
        for line in file:
            command = line.strip()
            responses = runCommand(library, command)
            for response in responses:
                print(response)

def runCommand(library, inputCommand):
    command, *options = inputCommand.split('*')
    if command == 'AddBook':
        return library.addBook(options[0], options[1], options[2], options[3], options[4])
    elif command == 'RemoveBook':
        return library.removeBook(options[0], options[1])
    elif command == 'BorrowBook':
        return library.borrowBook(options[0], options[1])
    elif command == 'ReturnBook':
        return library.returnBook(options[0], options[1])
    elif command == 'SearchBook':
        return library.searchBook(options[0], options[1])
    elif command == 'SearchBookTitle':
        return library.searchBookTitle(options[0])
    elif command == 'SearchBookAuthor':
        return library.searchBookAuthor(options[0])
    elif command == 'SearchBookISBN':
        return library.searchBookISBN(options[0])
    elif command == 'ListAvailableBooks':
        return library.listAvailableBooks()
    elif command == 'ListAvailableAuthors':
        return library.listAvailableAuthors()
    return []

def main():
    library = Library('Library.txt')
    processCommands(library, 'input.txt')
    library.updateLibrary()

