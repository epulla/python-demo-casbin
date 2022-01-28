from flask import Flask
from authorization.authorizator_decorator import authorizator

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/users")
@authorizator("users", "read")
def get_users():
    return f"<h3>You are allowed to make this request: get_users()</h3>"

@app.route("/create/user")
@authorizator("users", "write")
def create_user():
    return f"<h3>You are allowed to make this requests: create_user()</h3>"

@app.route("/activities")
@authorizator("activities", "read")
def get_activities():
    return f"<h3>You are allowed to make this requests: create_user()</h3>"

@app.route("/create/activity")
@authorizator("activities", "write")
def create_activity():
    return f"<h3>You are allowed to make this requests: create_user()</h3>"
