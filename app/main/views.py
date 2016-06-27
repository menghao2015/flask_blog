from flask import render_template, session, redirect, url_for, current_app, request, flash
from flask.ext.login import current_user, login_required
from .. import db
from ..models import User, Role, Post, Permission, Category, Comment, Lable
from ..email import send_email
from . import main
from .forms import NameForm, PostForm, CommentForm, CategoryForm, LableForm


@main.route('/', methods=['GET', 'POST'])
def index():
	post_test = Post.query.all()
	if post_test :
		lables = Lable.query.all()
		tag = Category.query.filter_by(name='technology').first()
		page = request.args.get('page', 1, type=int)
		pagination = Post.query.filter_by(category_id=tag.id).order_by(Post.timestamp.desc()).paginate(
					page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
		posts = pagination.items 
		return render_template('index.html', index=True,posts=posts, lables=lables,Post=Post,  pagination=pagination, mark='index')
	else:
		return render_template('empty_index.html')

@main.route('/lables/<int:lable_id>', methods=['GET', 'POST'])
def lables(lable_id):
	post_test = Post.query.all()
	if post_test :
		lables = Lable.query.all()
		lable = Lable.query.filter_by(id=lable_id).first()
		page = request.args.get('page', 1, type=int)
		pagination = Post.query.filter_by(lable_id=lable_id).order_by(Post.timestamp.desc()).paginate(
					page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
		posts = pagination.items 
		return render_template('index.html', index=True,posts=posts, lables=lables,Post=Post,  pagination=pagination, lable=lable, mark='lables')
	else:
		return render_template('empty_index.html')


@main.route('/all', methods=['GET', 'POST'])
def all():
	post_test = Post.query.all()
	if post_test :
		lables = Lable.query.all()
		page = request.args.get('page', 1, type=int)
		pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
					page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
		posts = pagination.items 
		return render_template('index.html', index=True,posts=posts, lables=lables,Post=Post,  pagination=pagination, mark='all')
	else:
		return render_template('empty_index.html')



@main.route('/mind_study', methods=['GET', 'POST'])
def mind_study():
	post_test = Post.query.all()
	if post_test :
		lables = Lable.query.all()
		tag = Category.query.filter_by(name='mind_study').first()
		page = request.args.get('page', 1, type=int)
		pagination = Post.query.filter_by(category_id=tag.id).order_by(Post.timestamp.desc()).paginate(
					page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
		posts = pagination.items 
		return render_template('index.html', index=True,posts=posts, lables=lables,Post=Post,  pagination=pagination, mark='mind_study')
	else:
		return render_template('empty_index.html')


@main.route('/others', methods=['GET', 'POST'])
def others():
	post_test = Post.query.all()
	if post_test :
		lables = Lable.query.all()
		tag = Category.query.filter_by(name='others').first()
		page = request.args.get('page', 1, type=int)
		pagination = Post.query.filter_by(category_id=tag.id).order_by(Post.timestamp.desc()).paginate(
					page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
		posts = pagination.items 
		return render_template('index.html', index=True,posts=posts, lables=lables,Post=Post,  pagination=pagination, mark='others')
	else:
		return render_template('empty_index.html')


@main.route('/bug', methods=['GET', 'POST'])
def bug():
	post_test = Post.query.all()
	if post_test :
		lables = Lable.query.all()
		tag = Category.query.filter_by(name='bug').first()
		page = request.args.get('page', 1, type=int)
		pagination = Post.query.filter_by(category_id=tag.id).order_by(Post.timestamp.desc()).paginate(
					page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
		posts = pagination.items 
		return render_template('index.html', index=True,posts=posts, lables=lables,Post=Post,  pagination=pagination, mark='bug')
	else:
		return render_template('empty_index.html')




@main.route('/new_post',  methods=['GET', 'POST'])
def new_post():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and \
		form.validate_on_submit():
		post = Post( title=form.title.data,category= Category.query.get(form.category.data), 
						lable = Lable.query.get(form.lable.data), body = form.body.data,
										author = current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	return render_template('new_post.html', form=form)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
	post = Post.query.get_or_404(id)
	form = CommentForm()
	lables = Lable.query.all()
	if form.validate_on_submit():
		comment = Comment(username=form.username.data, email=form.email.data,
							body=form.body.data, blog_web=form.blog_web.data, post=post)
		db.session.add(comment)
		flash('Your comment has been pushlished.')
		return redirect(url_for('.post', id=post.id)) 
	comments = post.comments.order_by(Comment.timestamp.asc())
	post.update_browsed()
	return render_template('post.html', posts=[post], form = form, post=post,Post=Post,  lables=lables, comments = comments ,edit_switch=True)



@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.lable = Lable.query.get(form.lable.data)
		post.category = Category.query.get(form.category.data)
		post.title = form.title.data
		post.body = form.body.data
		post.update_last_stamp()
		db.session.add(post)
		flash('The post has been updated.')
		return redirect(url_for('.post', id=post.id))
	form.title.data = post.title
	form.lable.data = post.lable_id
	form.category.data = post.category_id
	form.body.data = post.body
	return render_template('edit_post.html', form=form)

@main.route('/manager', methods=['GET', 'POST'])
@login_required
def manager():
	return render_template('manager.html')


@main.route('/manager/category', methods=['GET', 'POST'])
@login_required
def category():
	form = CategoryForm()
	categorys = Category.query.all()
	if request.method == 'POST':
		if 'add' in request.form.values():
			category_add = Category.query.filter_by(name=form.name.data).first()
			if not category_add:
				category = Category(name=form.name.data)
				db.session.add(category)
				flash('The Category has updated')
			else:
				flash('The Category has been exsit')
			return redirect(url_for('.category',form=form))

		elif 'del' in request.form.values(): 
			category_del = Category.query.filter_by(name=form.name.data).first()
			if category_del:
				db.session.delete(category_del)
				flash('The Category has been del.')
			else:
				flash('The category do not exsit')
			return redirect(url_for('.category',form=form))
	return render_template('manager.html', manager_swith='category', form=form, categorys=categorys)


@main.route('/manager/lable', methods=['GET', 'POST'])
@login_required
def lable():
	form = LableForm()
	lables = Lable.query.all()
	if request.method == 'POST':
		if 'add' in request.form.values():
			lable_add = Lable.query.filter_by(name=form.name.data).first()
			if not lable_add:
				lable = Lable(name=form.name.data)
				db.session.add(lable)
				flash('The Lable has updated')
			else:
				flash('The Lable has been exsit')
			return redirect(url_for('.lable',form=form))

		elif 'del' in request.form.values(): 
			lable_del = Lable.query.filter_by(name=form.name.data).first()
			if lable_del:
				db.session.delete(lable_del)
				flash('The Lable has been del.')
			else:
				flash('The lable do not exsit')
			return redirect(url_for('.lable',form=form))
	return render_template('manager.html', manager_swith='lable', form=form, lables=lables)


	

