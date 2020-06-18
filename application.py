import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

DATABASE_URL = "postgresql://postgres:zhaowenbo2305@localhost:5432/Books"

# engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

islogin = False
user_use = "Not logged in yet"


@app.route("/")
def index():
    global user_use
    # flights = db.execute("SELECT * FROM flights").fetchall()
    # users = db.execute("SELECT * FROM users").fetchall()
    # return render_template("index.html", flights=flights)
    return render_template("index.html", user_use=user_use)

# @app.route("/book", methods=["POST"])


@app.route("/register", methods=["POST"])
def register():
    global user_use
    input_username = request.form.get("input_username")
    input_password = request.form.get("input_password")
    # name = request.form.get("name")
    # try:
    #     flight_id = int(request.form.get("flight_id"))
    # except ValueError:
    #     return render_template("error.html", message="Invalid flight number.")

    # Make sure the flight exists.
    # if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
    if db.execute("SELECT * FROM users WHERE username = :input_username", {"input_username": input_username}).rowcount == 1:
        return render_template("error.html", message="This username has been registered!")
    # db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
    #         {"name": name, "flight_id": flight_id})
    db.execute("INSERT INTO users (username, password) VALUES (:input_username, :input_password)",
               {"input_username": input_username, "input_password": input_password})
    db.commit()
    return render_template("success.html", user_use=user_use)


@app.route("/login_jump", methods=["POST"])
def login_jump():
    global user_use
    return render_template("login.html", user_use=user_use)


@app.route("/register_jump", methods=["POST"])
def register_jump():
    global user_use
    return render_template("register.html", user_use=user_use)


@app.route("/search_jump", methods=["POST"])
def search_jump():
    global user_use
    global islogin
    if islogin == False:
        return render_template("login.html", user_use=user_use)
    return render_template("search.html", user_use=user_use)


@app.route("/homepage_jump", methods=["POST"])
def homepage_jump():
    global user_use
    return render_template("index.html", user_use=user_use)


@app.route("/login", methods=["POST"])
def login():
    global user_use
    global islogin

    input_username = request.form.get("input_username")
    input_password = request.form.get("input_password")

    if db.execute("SELECT * FROM users WHERE username = :input_username",
                  {"input_username": input_username}).rowcount == 0:
        return render_template("error.html", message="This account doesn't exist!")
    elif db.execute("SELECT * FROM users WHERE username = :input_username AND password= :input_password",
                    {"input_username": input_username, "input_password": input_password}).rowcount == 0:
        return render_template("error.html", message="Wrong password!")
    elif db.execute("SELECT * FROM users WHERE username = :input_username AND password= :input_password",
                    {"input_username": input_username, "input_password": input_password}).rowcount == 1:
        islogin = True
        user_use = input_username
        return render_template("userpage.html", user_use=user_use)


@app.route("/search", methods=["POST"])
def search():
    global user_use
    global islogin
    if islogin == False:
        return render_template("login.html", user_use=user_use)

    result = []
    result_isbn = []
    search_txt = request.form.get("input_text")

    if db.execute("SELECT isbn FROM books WHERE lower(title) like :search_txt", {"search_txt": '%' + search_txt.lower() + '%'}).rowcount != 0:
        result_isbn = result_isbn + db.execute("SELECT isbn FROM books WHERE lower(title) like :search_txt", {
                                               "search_txt": '%' + search_txt.lower() + '%'}).fetchall()
    if db.execute("SELECT isbn FROM books WHERE lower(author) like :search_txt", {"search_txt": '%' + search_txt.lower() + '%'}).rowcount != 0:
        result_isbn = result_isbn + db.execute("SELECT isbn FROM books WHERE lower(author) like :search_txt", {
                                               "search_txt": '%' + search_txt.lower() + '%'}).fetchall()
    if db.execute("SELECT isbn FROM books WHERE lower(isbn) like :search_txt", {"search_txt": '%' + search_txt.lower() + '%'}).rowcount != 0:
        result_isbn = result_isbn + db.execute("SELECT isbn FROM books WHERE lower(isbn) like :search_txt", {
                                               "search_txt": '%' + search_txt.lower() + '%'}).fetchall()

    if len(result_isbn) != 0:
        for i in range(0, len(result_isbn)):
            result_isbn[i] = result_isbn[i][0]
        result_isbn = set(result_isbn)  # 集合去重复
        for j in result_isbn:
            result = result + \
                db.execute("SELECT * FROM books WHERE isbn = :j",
                           {"j": j}).fetchall()
        return render_template("result.html", search_results=result, user_use=user_use)

    return render_template("error.html", message="No result")


@app.route("/result", methods=["POST"])
def details():
    global user_use
    global islogin
    if islogin == False:
        return render_template("login.html", user_use=user_use)

    s_isbn = request.form.get("selected_isbn")
    book_detail = db.execute(
        "SELECT * FROM books WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    # print(book_detail)
    book_detail = book_detail[0]
    review_results = db.execute(
        "SELECT * FROM reviews WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    review_count = db.execute(
        "SELECT COUNT(*) FROM reviews WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    review_count = review_count[0][0]
    return render_template("detail.html", isbn=book_detail[0], title=book_detail[1],
                           author=book_detail[2], year=book_detail[3], review_results=review_results, count=review_count, user_use=user_use)


@app.route("/detail", methods=["POST"])
def write_review():
    global user_use
    global islogin
    if islogin == False:
        return render_template("login.html", user_use=user_use)

    input_star = request.form.get("input_star")
    input_review = request.form.get("input_review")
    s_isbn = request.form.get("selected_isbn")
    # print(s_isbn)
    db.execute("INSERT INTO reviews (isbn, star, review) VALUES (:s_isbn, :input_star, :input_review)",
               {"s_isbn": s_isbn, "input_star": input_star, "input_review": input_review})
    db.commit()

    book_detail = db.execute(
        "SELECT * FROM books WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    # print(book_detail)
    book_detail = book_detail[0]
    review_results = db.execute(
        "SELECT * FROM reviews WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    review_count = db.execute(
        "SELECT COUNT(*) FROM reviews WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    review_count = review_count[0][0]

    return render_template("detail.html", isbn=book_detail[0], title=book_detail[1],
                           author=book_detail[2], year=book_detail[3], review_results=review_results, count=review_count, user_use=user_use)

    # return render_template("success.html", user_use=user_use)


@app.route("/logout", methods=["POST"])
def logout():
    global user_use
    global islogin
    if islogin == False:
        return render_template("login.html", user_use=user_use)

    elif islogin == True:
        islogin = False
        user_use = "Not logged in yet"
        return render_template("success.html", user_use=user_use)

@app.route("/detail/<s_isbn>")
def get_detail(s_isbn):
    if db.execute("SELECT * FROM books WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).rowcount == 0:
        return render_template("error.html", message="No such ISBN.")

    book_detail = db.execute(
        "SELECT * FROM books WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    book_detail = book_detail[0]
    review_results = db.execute(
        "SELECT * FROM reviews WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    review_count = db.execute(
        "SELECT COUNT(*) FROM reviews WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    review_count = review_count[0][0]
    return render_template("detail.html", isbn=book_detail[0], title=book_detail[1],
                           author=book_detail[2], year=book_detail[3], review_results=review_results, count=review_count, user_use=user_use)



from flask import Flask, render_template, jsonify, request

@app.route("/api/detail/<s_isbn>")
# def flight_api(flight_id):
def book_api(s_isbn):
    """Return details about a single flight."""

    if db.execute("SELECT * FROM books WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).rowcount == 0:
        return jsonify({"error": "Invalid ISBN"}), 422

    book_detail = db.execute(
        "SELECT * FROM books WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    book_detail = book_detail[0]

    review_results = db.execute(
        "SELECT * FROM reviews WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()

    review_count = db.execute(
        "SELECT COUNT(*) FROM reviews WHERE isbn = :s_isbn", {"s_isbn": s_isbn}).fetchall()
    review_count = review_count[0][0]

    return jsonify({
            "title": book_detail[1],
            "author": book_detail[2],
            "year": book_detail[3],
            "isbn": book_detail[0],
            "review_count": review_count
        })
