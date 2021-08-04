from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, \
    HiddenField, FormField, FieldList, Form, SelectMultipleField, widgets, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from chat_bot_package.database_tables import User
import json
import os


config_path = os.path.dirname(__file__)
configs = json.load(open(os.path.join(config_path, 'config/chatbot_config.json'), 'rb'))
TOPIC_CHOICES = configs['topic_choices']
SENTIMENT_CHOICES = configs['sentiment_choices']
STYLE_CHOICES = configs['style_choices']
BUTTONS = configs['buttons']


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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


class ReplyForm(Form):
    tweeter_id = HiddenField('شناسه')
    reply_content = TextAreaField('ریتوییت')
    topic_list = [(i, t) for i, t in enumerate(configs['topic_choices'])]
    r_topics = MultiCheckboxField('موضوع توییت', choices=topic_list, coerce=int)
    sentiments_choices = [(ist, s) for ist, s in enumerate(SENTIMENT_CHOICES)]
    reply_sentiment = RadioField('احساس توییت',
                                 choices=sentiments_choices,
                                 coerce=int)
    id_backup = StringField()


class LoginForm(FlaskForm):
    email = StringField('ایمیل آدرس', validators=[DataRequired(), Email()])
    password = PasswordField('پسورد', validators=[DataRequired()])
    remember_me = BooleanField('مرا به خاطر بسپارید')
    submit = SubmitField('ورود به سیستم')


class TweetForm(FlaskForm):
    id = HiddenField('شناسه', validators=[DataRequired()])
    tweet_content = TextAreaField('توییت بعدی', validators=[DataRequired()])
    topic_list = [(i, t) for i, t in enumerate(configs['topic_choices'])]
    topics = MultiCheckboxField('موضوع توییت', choices=topic_list, coerce=int)
    sentiments_choices = [(ist, s) for ist, s in enumerate(SENTIMENT_CHOICES)]
    tweet_sentiment = RadioField('احساس توییت',
                                 choices=sentiments_choices,
                                 coerce=int)
    replies = FieldList(FormField(ReplyForm), min_entries=0)
    submit = SubmitField(BUTTONS['save'])
    next = SubmitField(BUTTONS['reject'])


class ModelOutputs(FlaskForm):
    id = HiddenField('آیدی')
    dialogue = TextAreaField('دیالوگ', validators=[DataRequired()])
    response = TextAreaField('پاسخ اصلی', validators=[DataRequired()])
    submit = SubmitField('تایید ارزیابی')
