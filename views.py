from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from model import User, Series, Episode, requests, pq, add_series
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model



app = Flask(__name__)
app.config.from_object(config)

# Stuff to make login easier
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# End login stuff

# Adding markdown capability to the app
Markdown(app)

# @app.route("/")
# def index():
#     posts = Post.query.all()
#    return render_template("index.html", posts=posts)

# @app.route("/post/<int:id>")
# def view_post(id):
#     post = Post.query.get(id)
#     return render_template("post.html", post=post)

# @app.route("/post/new")
# @login_required
# def new_post():
#     return render_template("new_post.html")

# @app.route("/post/new", methods=["POST"])
# @login_required
# def create_post():
#     form = forms.NewPostForm(request.form)
#     if not form.validate():
#         flash("Error, all fields are required")
#         return render_template("new_post.html")

#     post = Post(title=form.title.data, body=form.body.data)
#     current_user.posts.append(post) 
    
#     model.session.commit()
#     model.session.refresh(post)

#     return redirect(url_for("view_post", id=post.id))



@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
    form = forms.LoginForm(request.form)
    if not form.validate():
        flash("Incorrect username or password") 
        return render_template("login.html")

    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()

    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("login.html")

    login_user(user)
    return redirect(request.args.get("next", url_for("index")))


@app.route("/")
def index():
    series = Series.query.all()
    return render_template("index.html")

@app.route("/search")
def search_page():
    return render_template("search.html")


@app.route("/search/results", methods = ["POST"])
def search_results():
    search_input = request.form.get("search")

    r = requests.get('http://thetvdb.com/api/GetSeries.php?seriesname='+search_input)
    xml_doc = r.text
    xml_doc = xml_doc.encode('utf-8')
    pyQ = pq(xml_doc, parser = 'xml')

    series = pyQ('Series')
    
    
    return render_template("search.html", series = series, pyQ =pyQ) # where series is xml


@app.route("/series/<external_series_id>")
def display_series_info(external_series_id):

    #is series already in database?
    count = model.session.query(Series).filter_by(external_id = external_series_id).count()

    if count == 0:
        add_series(series_external_id)
    series = model.session.query(Series).filter_by(external_id = external_series_id).one()

    return render_template("series_page.html", series = series) # where series is a db object

if __name__ == "__main__":
    app.run(debug=True)
