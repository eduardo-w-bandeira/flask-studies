from flask import Flask, request

app = Flask(__name__)

book_data = [
    {
        "id": 1,
        "name": "Something",
        "author_name": "Some Random Author",
        "year_published": 1997,
        "genre": "Drama",
    },
    {
        "id": 2,
        "name": "Important Book",
        "author_name": "Jordan Peterson",
        "year_published": 1990,
        "genre": "Philosophy",
    },
    {
        "id": 3,
        "name": "Abc",
        "author_name": "ZWY",
        "year_published": 1983,
        "genre": "Science Fiction",
    },
]


def view_data(data):
    string = ""
    for d_item in data:
        for key, value in d_item.items():
            string += f"{key}: {value}<br/>"
        string += "<br/>"
    return string


def order_books(data, order_by, order):
    if order_by:
        if order == 'asc':
            return sorted(data, key=lambda x: x[order_by])
        elif order == 'desc':
            return sorted(data, key=lambda x: x[order_by], reverse=True)
    return data


@app.route('/', methods=['GET'])
def home():
    return "Bla"


@app.route("/books", methods=["GET"])
def books():
    """GET /books?order_by=name&order=asc"""
    order_by = request.args.get('order_by')
    print("order_by:", order_by)
    order = request.args.get('order')
    print("order:", order)
    ordered_data = order_books(book_data, order_by, order)
    return view_data(ordered_data)


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    """GET /books/{id}"""
    for book in book_data:
        if book["id"] == book_id:
            return view_data([book])


@app.route("/books", methods=["POST"])
def add_book():
    new_book = request.json
    book_data.append(new_book)
    return "Book added successfully"


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    for book in book_data:
        if book["id"] == book_id:
            updated_book = request.json
            book.update(updated_book)
            return "Book updated successfully"


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    for i, book in enumerate(book_data):
        if book["id"] == book_id:
            del book_data[i]
            return f"Book #{book_id} deleted successfully"


if __name__ == '__main__':
    app.run(debug=True)
