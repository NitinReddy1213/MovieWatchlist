import uuid
from flask import render_template,Blueprint,session,redirect,request,current_app,url_for,flash
import secrets 
from movie_library.forms import movieform,ExtendedMovieform,RegisterForm,LoginForm
from movie_library.models import Movie , User 
from dataclasses import asdict 
import datetime
from passlib.hash import pbkdf2_sha256
pages = Blueprint("pages",__name__, template_folder = "templates", static_folder = "static")
import functools



def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))

        return route(*args, **kwargs)

    return route_wrapper


@pages.route('/')
@login_required
def index():
  user_data = current_app.db.user.find_one({"email": session["email"]})
  user = User(**user_data)    #here we are unpacking the data from the database and storing it in a user object
  movie_data = current_app.db.movie.find({"_id": {"$in": user.movies}})
  movies = [Movie(**movie) for movie in movie_data]#here we have used a method to unpack the dictionary data and store it in list elements

  return render_template("index.html",title = "Movies Watchlist",movie_data = movies) # we are passing the movie data to front end


@pages.route("/add", methods = ["GET","POST"])
@login_required

def add():
  form = movieform()

  if form.validate_on_submit():
    movie =  Movie(_id = uuid.uuid4().hex,
              title = form.title.data,
              director = form.director.data,
              year = form.year.data,
    )
    current_app.db.movie.insert_one(asdict(movie))
    current_app.db.user.update_one({"_id": session["user_id"]}, {"$push": {"movies": movie._id}}) #this is done to add the movie to the user list everytime 
    #a movie is created in the user's index page.

  
    return redirect(url_for(".movie", _id=movie._id))


  return render_template("new_movie.html",title = "Add New Movie",form=form )


#last section extended form part

@pages.route("/edit/string/<string:_id>", methods = ["GET","POST"])
@login_required

def edit_movie(_id : str):
  movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
  form = ExtendedMovieform(obj=movie)
  if form.validate_on_submit():
    movie.cast = form.cast.data
    movie.series = form.series.data
    movie.tags = form.tags.data
    movie.description = form.description.data
    movie.video_link = form.video_link.data

    current_app.db.movie.update_one({"_id": _id}, {"$set": asdict(movie)})
    return redirect(url_for(".movie", _id=_id))
  return render_template('movieform.html', movie = movie ,form = form )


#these are the minute updates which we are making to the system to display movie content and all of them are taking in values
#these values are update in the databse and shon again in the front end 
#so that is the reason they take in necessary inputs using pythons datatypes creation.

##all of these functions belong to the same page check the endpoints

@pages.get("/movie/<string:_id>")  #here we are passing the end points from a single page# these can be used to update the existing values in the database.
def movie(_id: str):
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
    return render_template("movie_details.html", movie=movie)   #this functionality is added to get the details of the movie from the details pages
#acts more like a get request new concept for a python generator ro fetch data from databse.


@pages.get("/movie/<string:_id>/rate")
@login_required
def rate_movie(_id):
    rating = int(request.args.get("rating"))
    current_app.db.movie.update_one({"_id": _id}, {"$set": {"rating": rating}})

    return redirect(url_for(".movie", _id=_id)) #changed from rate_movie to movie 

@pages.get("/movie/<string:_id>/watch")
@login_required
def watch_today(_id):
  current_app.db.movie.update_one({"_id": _id}, {"$set": {"last_watched": datetime.datetime.today()}})
  
  
  return redirect(url_for(".movie",_id = _id))


@pages.get("/toggle-theme")

def toggle_theme():
  current_theme = session.get("theme")
  if current_theme == "dark":
    session["theme"] = "light"
  else:
    session['theme'] = "dark"
    
  return redirect(request.args.get("current_page")) # this has been done to stay in the same pages


#registration and login part of the application 

@pages.route("/register",methods = ["GET","POST"])

def register():
  if session.get("email"):
    return redirect(url_for(".login"))
  
  form = RegisterForm()

  if form.validate_on_submit():
    user = User(_id = uuid.uuid4().hex,
                email = form.email.data,
                password = pbkdf2_sha256.hash(form.password.data)
    )
    current_app.db.user.insert_one(asdict(user))
    
    flash("You have successfully registered","success")

  return render_template("register.html",title = "movies Watchlist",form=form)

@pages.route("/login",methods = ["GET","POST"])
def login():
  if session.get("email"):
    return redirect(url_for(".index"))   #similar to the above function but we do an error checkiing
  form = LoginForm()

  if form.validate_on_submit():
    user_data = current_app.db.user.find_one({"email": form.email.data})
    if not user_data:
      flash("invalid Usernae/Password Or user doesnt exist",category = "danger")
      return redirect(url_for(".login"))
    
    user = User(**user_data)

    if user and pbkdf2_sha256.verify(form.password.data, user.password):
      session["user_id"] = user._id
      session["email"] = user.email
      flash("You have successfully logged in","success")
      return redirect(url_for(".index"))
    
    flash("invalid Usernae/Password Or user doesnt exist",category = "danger")
    
  return render_template("login.html",title = "movies Watchlist",form=form)
  

  @pages.route("/logout")
  def logout():
    session.clear()
    session["theme"] = current_theme

    return redirect(url_for(".login"))