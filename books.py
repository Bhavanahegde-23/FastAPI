from fastapi import FastAPI , Body


app = FastAPI()

BOOKS = [
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Fiction"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "category": "Romance"},
    {"title": "Moby-Dick", "author": "Herman Melville", "category": "Adventure"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy"},
    {"title": "The Hobbit 2", "author": "J.R.R. Tolkien", "category": "Fantasy"},
    {"title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez", "category": "Magical Realism"},
]

@app.get("/books/")
async def read_books():
    return BOOKS

# @app.get("/book/mybook")
# async def read_my_book():
#     my_book = {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Fiction"}
#     return my_book

@app.get("/books/{category}")
async def read_books_by_category(category: str):
    filtered_books = [book for book in BOOKS if book["category"].lower() == category.lower()]
    return filtered_books

@app.get("/books/{author}/{category}")
async def read_books_by_author(author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author", "").lower() == author.lower() and \
        book.get("category", "").lower() == category.lower():
            books_to_return.append(book)
    return books_to_return

#Post method --> it is create method 
@app.post("/books/create_book")
async def creat_new_book(new_book = Body()):
    BOOKS.append(new_book)
    return new_book


# Put method --> it is update method -exactly looks like body of the post but 
# we are gonna send whats there and update the value of that book
@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == updated_book["title"].casefold():
            BOOKS[i] = updated_book
            return BOOKS[i]
    return {"error": "Book not found"}


# Delete method --> it is delete method 
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == book_title.casefold():
            deleted_book = BOOKS.pop(i)
            return deleted_book
    return {"error": "Book not found"}

#fetch all the books from perticular author
@app.get("/books/author/{author_name}")
async def read_books_by_author_name(author_name: str):
    author_books = [book for book in BOOKS if book["author"].lower() == author_name.lower()]
    return author_books
