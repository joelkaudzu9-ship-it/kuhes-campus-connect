# app/forms.py - COMPLETE VERSION
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    faculty = SelectField('Faculty', choices=[
        ('', 'Select Faculty'),
        ('medicine', 'Medicine'),
        ('pharmacy', 'Pharmacy'),
        ('nursing', 'Nursing'),
        ('public_health', 'Public Health'),
        ('biomedical', 'Biomedical Sciences'),
        ('dentistry', 'Dentistry'),
        ('allied_health', 'Allied Health Sciences')
    ], validators=[DataRequired()])
    program = StringField('Program', validators=[DataRequired()])
    year = SelectField('Year of Study', choices=[
        ('', 'Select Year'),
        ('1', 'Year 1'),
        ('2', 'Year 2'),
        ('3', 'Year 3'),
        ('4', 'Year 4'),
        ('5', 'Year 5'),
        ('6', 'Year 6'),
        ('intern', 'Intern'),
        ('postgrad', 'Postgraduate'),
        ('staff', 'Staff'),
        ('faculty', 'Faculty')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('', 'Select Category'),
        ('news', 'Campus News'),
        ('announcement', 'Announcement'),
        ('event', 'Event'),
        ('question', 'Question'),
        ('discussion', 'Discussion'),
        ('resource', 'Resource Share'),
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('religious', 'Religious'),
        ('social', 'Social'),
        ('study_group', 'Study Group'),
        ('job', 'Job Opportunity'),
        ('housing', 'Housing'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    submit = SubmitField('Create Post')


class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Post Comment')


class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_type = SelectField('Event Type', choices=[
        ('', 'Select Type'),
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('religious', 'Religious'),
        ('social', 'Social'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('conference', 'Conference'),
        ('career', 'Career Fair'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('', 'Select Category'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('competition', 'Competition'),
        ('celebration', 'Celebration'),
        ('conference', 'Conference'),
        ('exhibition', 'Exhibition'),
        ('lecture', 'Lecture'),
        ('meeting', 'Meeting')
    ], validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired(), Length(max=200)])
    organizer_name = StringField('Organizer Name', validators=[Optional(), Length(max=100)])
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    contact_phone = StringField('Contact Phone', validators=[Optional(), Length(max=20)])
    start_date = StringField('Start Date (YYYY-MM-DD)', validators=[DataRequired()])
    start_time = StringField('Start Time (HH:MM)', validators=[DataRequired()])
    end_date = StringField('End Date (YYYY-MM-DD)', validators=[Optional()])
    end_time = StringField('End Time (HH:MM)', validators=[Optional()])
    submit = SubmitField('Create Event')


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


class ProfileUpdateForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    faculty = SelectField('Faculty', choices=[
        ('medicine', 'Medicine'),
        ('pharmacy', 'Pharmacy'),
        ('nursing', 'Nursing'),
        ('public_health', 'Public Health'),
        ('biomedical', 'Biomedical Sciences'),
        ('dentistry', 'Dentistry'),
        ('allied_health', 'Allied Health Sciences')
    ], validators=[DataRequired()])
    program = StringField('Program', validators=[DataRequired()])
    year = SelectField('Year of Study', choices=[
        ('1', 'Year 1'),
        ('2', 'Year 2'),
        ('3', 'Year 3'),
        ('4', 'Year 4'),
        ('5', 'Year 5'),
        ('6', 'Year 6'),
        ('intern', 'Intern'),
        ('postgrad', 'Postgraduate'),
        ('staff', 'Staff'),
        ('faculty', 'Faculty')
    ], validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Profile')