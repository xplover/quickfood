from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import InputRequired, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    user_id = StringField("User_id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Repeat password:",
                              validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    user_id = StringField("User_    id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")


class FoodSearch(FlaskForm):
    dish = StringField("Search for a Dish")
    restaurant = SelectField("Select a Restaurant",
                             choices=[("Select a Restaurant", "Select a Restaurant"),
                                      ("La Cucina Italian Restaurant",
                                       "La Cucina Italian Restaurant"),
                                      ("Shanghai Chinese Restaurant",
                                       "Shanghai Chinese Restaurant"),
                                      ("Spicy Indian Restaurant", "Spicy Indian Restaurant"), ])
    submit = SubmitField("Submit")


class CheckoutForm(FlaskForm):
    address = StringField("Address", validators=[InputRequired()])
    phone = IntegerField("Phone", validators=[
        InputRequired()])
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    name = StringField("Name")
    comment = StringField("Comment")
    submit = SubmitField("Submit")
