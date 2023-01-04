from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import Users
from flask_login import current_user
from datetime import date

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=20), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            print('Error')
            raise ValidationError('Username taken. Please choose a different username!')
    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already registered. Please try to Login!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg','jpg','png'])])
    print(picture.name)
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data!=current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username taken. Please choose a different username!')
    def validate_email(self, email):
        if email.data!=current_user.email:
            email = Users.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already registered. Please try to Login!')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class AeroBookingForm(FlaskForm):
    sourceState = SelectField('Source State', choices=[], validators=[DataRequired()])
    destState = SelectField('Destination State', choices=[], validators=[DataRequired()])
    sourceCity = SelectField('Source City', choices=[], validators=[DataRequired()])
    destCity = SelectField('Destination City', choices=[], validators=[DataRequired()])
    travelDate = DateField('Travel Date', validators=[DataRequired()])
    submit = SubmitField('Book')

    def validate_travelDate(self, travelDate):
        if travelDate.data<date.today():
            print('Start date Excpetion')
            raise ValidationError('Start date is before today!')

class BusBookingForm(FlaskForm):
    sourceState = SelectField('Source State', choices=[], validators=[DataRequired()])
    destState = SelectField('Destination State', choices=[], validators=[DataRequired()])
    sourceCity = SelectField('Source City', choices=[], validators=[DataRequired()])
    destCity = SelectField('Destination City', choices=[], validators=[DataRequired()])
    travelDate = DateField('Travel Date', validators=[DataRequired()])
    submit = SubmitField('Book')

    def validate_travelDate(self, travelDate):
        if travelDate.data<date.today():
            print('Start date Excpetion')
            raise ValidationError('Start date is before today!')

class HotelBookingForm(FlaskForm):
    state = SelectField('State', choices=[], validators=[DataRequired()])
    city = SelectField('City', choices=[], validators=[DataRequired()], validate_choice=False)
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Book')
    def validate_start_date(self, start_date):
        if start_date.data<date.today():
            print('Start date Excpetion')
            raise ValidationError('Start date is before today!')
    def validate_end_date(self, end_date):
        if self.start_date and self.start_date.data>end_date.data:
            print('End date Excpetion')
            raise ValidationError('Please select End Date greater than Start Date!')

