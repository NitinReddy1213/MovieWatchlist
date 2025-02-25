from flask_wtf import FlaskForm 
from wtforms import IntegerField,StringField,SubmitField,TextAreaField,URLField,PasswordField
from wtforms.validators import InputRequired,NumberRange,Email,Length,EqualTo


class movieform(FlaskForm):
  title = StringField("Title",validators = [InputRequired()])
  director = StringField("director",validators = [InputRequired()])
  year = IntegerField("year",validators = [InputRequired(),NumberRange(min = 1878, message = "Please enter year in MM-DD-YYYY")] )
  submit = SubmitField("Add movie")



class StringListField(TextAreaField):
  def _value(self):
    if self.data:
      return "\n".join(self.data)    #udnerstand this code later
  def process_formdata(self, valuelist):
    if valuelist and valuelist[0]:
      self.data = [line.strip() for line in valuelist[0].split("\n")]
    else:
      self.data = []


class ExtendedMovieform(movieform):
  cast = StringListField("cast")
  series = StringListField("series")
  tags = StringListField("tags")
  description = TextAreaField("description")
  video_link = URLField("video_link")

  submit = SubmitField("submit")


class RegisterForm(FlaskForm):
  email = StringField("Email",validators = [InputRequired(),Email()])
  password = PasswordField("password",validators = [InputRequired(),Length(min = 4,max=20,message = "Your password must be between 4 and 20 characters")])
  confirm_password = PasswordField("confirm Password",validators = [InputRequired(),EqualTo("password",message = "this password did not match the above password ")])
  submit = SubmitField("submit")

class LoginForm(FlaskForm):
  email = StringField("Email",validators = [InputRequired(),Email()])
  password = PasswordField("password",validators = [InputRequired(),Length(min = 4,max=20,)])
  submit = SubmitField("submit")
