#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Category, Comment, Post, Lable
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'unix')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Category=Category, Comment=Comment, Post=Post, Lable=Lable)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
	"""Run deployment tasks."""
	''' run this command in the first times '''
	db.create_all()
	Role.insert_roles()
	Category.insert_categorys()
	Lable.insert_lables()

if __name__ == '__main__':
	manager.run()
