from flask import Flask, render_template, redirect, url_for, flash, abort, session, g
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from wtforms import StringField, SubmitField, PasswordField
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os



from flask_login import UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
db.create_all()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return render_template("not_admin.html")
        return f(*args, **kwargs)
    return decorated_function

def loggedin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Log in to have access to the post!")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    file_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

db.create_all()

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    file_url = StringField("File URL", validators=[DataRequired(), URL()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form, current_user=current_user)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        file_url=post.file_url,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.file_url = edit_form.file_url
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=['GET', 'POST'])
@admin_only
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            file_url=form.file_url.data,
            author=form.author.data,
            date=date.today().strftime("%B %d, %Y")
        )

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                print(User.query.filter_by(email=form.email.data).first())
                #User already exists
                flash("You've already signed up with that email, log in instead!")
                return redirect(url_for('login'))

            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=form.email.data,
                name=form.name.data,
                password=hash_and_salted_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form, current_user=current_user)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

