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