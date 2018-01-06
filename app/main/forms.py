#-*-coding:utf-8 -*-
from flask import session, current_app, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, ValidationError
from wtforms.validators import Required, Length, Email,URL
from flask_pagedown.fields import PageDownField
from ..models import Lable, Category


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
	title = PageDownField('Title', validators=[Required()])
	lable = SelectField('Lable', coerce=int)
	category = SelectField('Category', coerce=int)
	body = PageDownField("Post body", validators=[Required()])
	submit = SubmitField('Submit')

	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.lable.choices = [ (lable.id, lable.name)
							for lable in Lable.query.all()]
		self.category.choices = [ (category.id, category.name)
							for category in Category.query.all()]
	


class CommentForm(FlaskForm):
	body = TextAreaField('comment-body', validators=[Required(), Length(1, 512)])
	username = StringField('username', validators=[Required(), Length(1,64) ])
	email = StringField('email ', validators=[Required(), Length(1,64), Email()])
	blog_web = StringField('personal web', validators=[ Length(0, 64)])
	recaptcha = StringField('verification code', validators=[ Required(), Length(4, 4)])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Biu ~~')

	def validate_recaptcha(self, field):
		if session.get('captcha') != field.data.upper():
			#flash(u'验证码错误') 	
			raise ValidationError('Recaptha Error') 	



class CategoryForm(FlaskForm):
	name = StringField('Add/Del Category Name', validators=[Required(), Length(1,64) ])

class LableForm(FlaskForm):
	name = StringField('Add/Del Lable Name', validators=[Required(), Length(1,64) ])

