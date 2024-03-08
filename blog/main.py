from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

posts = []


def find_post(id):
    found = False
    for post in posts:
        if post["id"] == id:
            found = True
            break
    if not found:
        return False
    return post


@app.route("/")
def home():
    action_title = "All Posts" if posts else "No Posts"
    return render_template("home.html", action_title=action_title,  posts=posts)


@app.route("/create", methods=["GET", "POST"])
def create_post():
    global posts
    if request.method == "GET":
        return render_template("create_post.html", action_title="Create New Post")
    if not len(posts):
        id = 1
    else:
        id = posts[-1]["id"] + 1
    post = {
        "id": id, "title": request.form['title'], "content": request.form['content']}
    posts.append(post)
    return redirect(url_for("home"))


@app.route("/post_detail/<int:id>")
def post_detail(id):
    post = find_post(id)
    if not post:
        return redirect(url_for("home"))
    return render_template("post_detail.html", post=post)


@app.route("/edit_post/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post = find_post(id)
    if not post:
        return redirect(url_for("home"))
    if request.method == "GET":
        return render_template("edit_post.html", post=post)
    post["title"] = request.form["title"]
    post["content"] = request.form["content"]
    return redirect(url_for("post_detail", id=id))


@app.route("/delete/<int:id>")
def delete_post(id):
    post = find_post(id)
    if not post:
        return redirect(url_for("home"))
    for index, item in enumerate(posts):
        if item is post:
            posts.pop(index)
            return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
