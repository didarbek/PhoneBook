from flask import (Flask, request, jsonify,
                   render_template, url_for, flash,
                   redirect, abort, Response)
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse


# defining our flask application
app = Flask(__name__)

# setting our config file
app.config.from_object("project.config.Config")

# creating db instance with SQLAlchemy agent
db = SQLAlchemy(app)


# Users model containing fields - id (primary key, unique), name (), phone
class Users(db.Model):
    # specifying the name of table
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.Integer(), nullable=False)

    # special method to get json format
    @property
    def serialize(self):
       # return object data in easily serializable format
       return {
           'user_id': self.id,
           'name': self.name,
           'phone': self.phone
       }

    # Initializing User model
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


# api view to show all our users
# returns json with format [
#  {
#   "user_id": "[UNIQUE_USER_ID]",
#   "name": "[USER_NAME]",
#   "phone": "[PHONE_NUMBER]"
#  },
#  {
#   "user_id": "[UNIQUE_USER_ID]",
#   "name": "[USER_NAME]",
#   "phone": "[PHONE_NUMBER]"
#  },
#  …
# ]
@app.route('/user/list', methods=["GET"])
def users_list():

    return jsonify([i.serialize for i in Users.query.all()])


# api endpoint to add the user
# returns json with format {"user_id": "[UNIQUE_USER_ID]", "operation_type": "add", "operation_status": "[fail | success]"}
@app.route('/user/add', methods=["POST"])
def user_add():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone']

            user = Users(name, phone)

            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return jsonify({"user_id": user.id, "operation_type": "add", "operation_status": "fail"})

    return jsonify({"user_id": user.id, "operation_type": "add", "operation_status": "success"})


# api endpoint to edit the user
# returns json with format {"user_id": "[UNIQUE_USER_ID]", "operation_type": "edit", "operation_status": "[fail | success]"}
@app.route('/user/edit/<int:user_id>', methods=["PUT"])
def user_edit(user_id):
    user = Users.query.get(user_id)

    if user is None:
        abort(404)

    user.name = request.form['name']
    user.phone = request.form['phone']

    db.session.commit()

    return jsonify({"user_id": user.id, "operation_type": "edit", "operation_status": "success"})


# api endpoint to delete the user
# returns json with format {"user_id": "[UNIQUE_USER_ID]", "operation_type": "delete", "operation_status": "[fail | success]"}
@app.route('/user/delete/<int:user_id>', methods=["DELETE"])
def user_delete(user_id):
    user = Users.query.get(user_id)

    if user is None:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"user_id": user.id, "operation_type": "delete", "operation_status": "success"})


# endpoint to show if application is running and connection with database is established
@app.route('/status', methods=['GET'])
def status():
    try:
        result = db.engine.execute('SELECT 1')
        if result:
            return jsonify({"status": "OK"}), 200
    except Exception as e:
        app.logger.exception(e)

    return jsonify({"status": "Error"}), 500


# creating feature to list all users in frontend
# it just renders a template and passes our context parameters (users=users)
@app.route('/')
def index():
    users = Users.query.all()

    return render_template('index.html', users=users, hostname=urlparse(request.base_url).hostname)

