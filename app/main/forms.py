from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email,URL
from flask.ext.pagedown.fields import PageDownField
from ..models import Lable, Category


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PostForm(Form):
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
	


class CommentForm(Form):
	body = TextAreaField('tips-body', validators=[Required(), Length(1, 512)])
	username = StringField('tips-name', validators=[Required(), Length(1,64) ])
	email = StringField('tips-Email ', validators=[Required(), Length(1,64), Email()])
	blog_web = StringField('tips-web', validators=[ Length(0, 64)])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('submit')

class CategoryForm(Form):
	name = StringField('Add/Del Category Name', validators=[Required(), Length(1,64) ])

class LableForm(Form):
	name = StringField('Add/Del Lable Name', validators=[Required(), Length(1,64) ])

