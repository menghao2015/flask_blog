from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach, re




class Permission:
	FOLLOW = 0x01
	COMMENT = 0x02
	WRITE_ARTICLES = 0x04
	MODERATE_COMMENTS = 0x08
	ADMINISTER = 0x80

class Lable(db.Model):
	__tablename__ = 'lables'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True, index=True)
	lables = db.relationship('Post', backref='lable', lazy='dynamic')

class Category(db.Model):
	__tablename__ = 'categorys'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64),unique=True, index=True)
	categorys = db.relationship('Post', backref='category', lazy='dynamic')

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64))
	username = db.Column(db.String(64))
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	blog_web = db.Column(db.String(128))
	disabled = db.Column(db.Boolean)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
		              'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify(bleach.clean(
			markdown(value, output_format='html'), tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128))
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	body_head = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	last_stamp = db.Column(db.DateTime, default=datetime.utcnow)
	browsed = db.Column(db.Integer,default=0)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
	lable_id = db.Column(db.Integer, db.ForeignKey('lables.id'))
	comments = db.relationship('Comment', backref='post', lazy='dynamic')


	def update_last_stamp(self):
		self.last_stamp = datetime.utcnow()
		db.session.add(self)
	
	def update_browsed(self):
		self.browsed = self.browsed + 1
		db.session.add(self)
	
	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
			'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']

		target.body_html = bleach.linkify(bleach.clean(
				markdown(value, output_format='html'), tags=allowed_tags, strip=True))

	@staticmethod
	def changed_body_head(self,body, *args, **kwargs):
		self.body_head = body[0:500]
		dr = re.compile(r'<[^>]+>',re.S)
		self.body_head = dr.sub('',self.body_head)
		db.session.add(self)
	
	@staticmethod
	def update_all_body_head():
		posts = Post.query.all()
		for post in posts:
			post.body_head = post.body[0:500]
			dr = re.compile(r'<[^>]+>',re.S)
			post.body_head = dr.sub('',post.body_head)
			db.session.add(post)
		db.session.commit()
			
			
db.event.listen(Post.body, 'set', Post.changed_body_head)	
db.event.listen(Post.body, 'set', Post.on_changed_body)	
	

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')

	@staticmethod
	def insert_roles():
		roles = {
			'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES |
														Permission.MODERATE_COMMENTS, False),
			'Administrator': (0xff, False),
			'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True)
		}

		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()


	def __repr__(self):
		return '<Role %r>' % self.name


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')


	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def can(self, permissions):
		return self.role is not None and  (self.role.permissions & permissions) == permissions
	def is_administrator(self):
		return self.can(Permission.ADMINISTER)


	def __repr__(self):
		return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


