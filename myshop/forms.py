from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, validators, DateField
from wtforms.validators import DataRequired, \
    EqualTo, ValidationError
from myshop.models import User


class RegisterForm(FlaskForm):   
    username = StringField('name', [validators.DataRequired('Please enter your username'), validators.Length(min=3, max=15)])
    password = PasswordField('New password',
                             [validators.DataRequired(), validators.Regexp('^.{6,14}$',
                                                                    message="Your password should be between 6 and 14 characters long.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=35)])
    submit = SubmitField('Register')
    recaptcha = RecaptchaField()

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already exist. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('username', [validators.DataRequired('Please enter your username'), validators.Length(min=4, max=15)])
    password = PasswordField('password', [validators.DataRequired('Please enter your password'), validators.Length(min=6, max=14)])
    submit = SubmitField('Login')
    recaptcha = RecaptchaField()


class ContactUs(FlaskForm):
    name = StringField('name',
                           [validators.DataRequired('Please enter an username'), validators.Length(min=3, max=10)])
    content = StringField('Content', [validators.DataRequired('Please enter your enquiry here'), validators.Length(min=6, max=1000)])
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    content = StringField('text',
                          [validators.DataRequired('Please enter your message')])
    rating = StringField('',
            [validators.DataRequired('Please enter a rating from 1 to 5')])
    submit = SubmitField('Submit')


class BillingInfo(FlaskForm):
    first_name = StringField('First Name',
                           [validators.DataRequired('Please enter your first name'), validators.Length(min=3, max=15)])
    last_name = StringField('Last Name',[validators.DataRequired('Please enter your last name'),
                                         validators.Length(min=3, max=15)])

    credit_card_num = IntegerField('Credit Card Number',
                          [validators.DataRequired('Please enter your credit card number'), validators.Length(min=15,
                                                                                                             max=16)])

    billing_addr = StringField('Billing address',[validators.DataRequired('Please enter your billing address')])
    bill_date = DateField("Today's date",
                          [validators.DataRequired("Please enter today's date")],format='%d/%m/%Y')
    credit_card_expiry = DateField("Card expiry date",
                          [validators.DataRequired("Please enter your card's expiry date")], format='%d/%m/%Y')
    submit = SubmitField('Pay now')



