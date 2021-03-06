import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from database import db
from forms import ExtendedRegisterForm


app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

# create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GROUNDTRUTH_FOLDER'], exist_ok=True)

# Setup flask-security
from models import Role, User, Competition, Submission
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

# Create admin role and user
@app.before_first_request
def create_default_role_and_user():
    if User.query.count() == 0:
        user_datastore.create_role(name='admin')
        user_datastore.create_user(username='admin', email='admin@example.com',
                password='changeme', firstname="admin_firstname",
                lastname="admin_lastname", active=True, roles=['admin'])
        db.session.commit()

# Setup flask-admin
from views import AdminModelView, UserAdmin, CompetitionAdmin, MyAdminIndexView
admin = Admin(app, name='Submission', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(AdminModelView(Role, db.session))
admin.add_view(UserAdmin(User, db.session))
admin.add_view(CompetitionAdmin(Competition, db.session))
admin.add_view(AdminModelView(Submission, db.session))

