from fastapi import FastAPI, Body ,Path ,Query , HTTPException
from TodoApp.BooksExp.book_data import BOOK , BookRequest



app = FastAPI()

BOOKS = [
    BOOK(id=1, title="The Catcher in the Rye", author="J.D. Salinger", category="Fiction", description="A story about adolescent Holden Caulfield's disillusionment with the adult world.", rating=4, year=1951),
    BOOK(id=2, title="Pride and Prejudice", author="Jane Austen", category="Romance", description="A classic novel exploring themes of love, reputation, and class in 19th century England.", rating=5, year=1813),
    BOOK(id=3, title="Moby-Dick", author="Herman Melville", category="Adventure", description="The narrative of Captain Ahab's obsessive quest to kill the white whale Moby Dick.", rating=4, year=1851),
    BOOK(id=6, title="1984", author="George Orwell", category="Dystopian", description="A chilling dystopia about surveillance and totalitarianism.", rating=5, year=1949),
    BOOK(id=7, title="To Kill a Mockingbird", author="Harper Lee", category="Fiction", description="A young girl's perspective on racial injustice in the American South.", rating=5, year=1960),
    BOOK(id=8, title="The Hobbit", author="J.R.R. Tolkien", category="Fantasy", description="Bilbo Baggins's adventurous quest to win a share of treasure guarded by a dragon.", rating=5, year=1937),
    BOOK(id=9, title="The Great Gatsby", author="F. Scott Fitzgerald", category="Fiction", description="A critique of the American Dream set in the Roaring Twenties.", rating=4, year=1925),
    BOOK(id=10, title="Brave New World", author="Aldous Huxley", category="Science Fiction", description="A satirical look at a technologically advanced future society.", rating=4, year=1932),
]

#For getting all books
@app.get("/books/")
async def read_books():
    return BOOKS

#for creating a new book
@app.post("/books/create_book")
async def create_new_book(new_book: BOOK = Body()):
    BOOKS.append(new_book)
    return new_book

#Get the book based on year
@app.get("/books/{year}")
async def get_books_by_year(year:int):
    match = [book for book in BOOKS if book.year == year]
    if match:
        return match
    raise HTTPException(status_code=404, detail="No books found for the given year")

#Find book ID
def find_book_id(book: BOOK):
    book.id = 1 if len(BOOKS) == 0 else  BOOKS[-1].id + 1
    return book


#Create method with validation
@app.post("/books/create_book_validated")
async def create_book_validated(book_request: BookRequest):
    new_book = BOOK(**book_request.dict())
    BOOKS.append(find_book_id(new_book))
    return new_book

#Get the books by ID
@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int = Path(gt = 0) ):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}

#Get the books by rating

@app.get("/books/rating/{book_rating}")
async def get_books_by_rating(book_rating: int ):
    matched_books = [book for book in BOOKS if book.rating == book_rating]
    return matched_books
#for updating a book by ID
@app.put("/books/update_book/{book_id}")
async def update_book(book_id: int, updated_book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            # Convert BookRequest to BOOK object, keeping the original ID
            updated_data = updated_book.dict()
            updated_data['id'] = book_id  # Keep the original ID
            BOOKS[i] = BOOK(**updated_data)
            return BOOKS[i]
    return {"error": "Book not found"}

#for deleting a book
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].title.casefold() == book_title.casefold():
            deleted_book = BOOKS.pop(i)
            return {"message": "Book deleted successfully", "book": deleted_book}
    return {"error": "Book not found"}




