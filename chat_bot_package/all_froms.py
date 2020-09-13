from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from chat_bot_package.database_tables import User


class RegistrationForm(FlaskForm):
    username = StringField('شناسه کاربری', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('ایمیل آدرس', validators=[DataRequired(), Email()])
    password = PasswordField('پسورد', validators=[DataRequired()])
    confirm_password = PasswordField('تایید پسورد', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('ثبت نام')

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('ایمیل شما موجود است')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('شناسه کاربری شما موجود است')


class LoginForm(FlaskForm):
    email = StringField('ایمیل آدرس', validators=[DataRequired(), Email()])
    password = PasswordField('پسورد', validators=[DataRequired()])
    remember_me = BooleanField('مرا به خاطر بسپارید')
    submit = SubmitField('ورود به سیستم')
