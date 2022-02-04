# Python demo with Casbin library
Casbin is a open-source access control library. It provides support for enforcing authorization based on various access control models.

# Content

- [Installation](https://github.com/epulla/python-demo-casbin#installation)
- [How it works](https://github.com/epulla/python-demo-casbin#how-it-works)
- [Url examples for testing the app](https://github.com/epulla/python-demo-casbin#url-tests)
- Pros & Cons of Casbin/Casdoor

# Installation

## Requirements

- Python <= 3.8

## Setup

You need to have installed python virtual environment. See docs [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv)


First, create a python virtual environment (env) in the root directory:

```bash
python3 -m venv env # Linux, Mac
py -m venv env # Windows
```

Activate the virtual environment:

```bash
source env/bin/activate # Linux, Mac
.\env\Scripts\activate # Windows
```

Install requirements in a virtual environment:

```bash
python3 -m pip install -r requirements.txt # Linux, Mac
py -m pip install -r requirements.txt # Windows
```


## Run the flask app

Set the FLASK_APP variable:

```bash
export FLASK_APP=main # Linux, Mac
set FLASK_APP=main # Windows
```

Run the flask app:

```
flask run
```

Go to [URL test](https://github.com/epulla/python-demo-casbin#url-tests) section to test some urls after running flask.

# How it works

## Casbin model configuration file

In the directory casbin_files/models, there are .conf files that describes the authorization model that it will follow. See more [here](https://casbin.org/docs/en/supported-models).

In this example, we will follow the **RBAC with roles** authorization model. This model allows us to describes roles and the resources that a role can access. It also helps us to create groups of resources, so a role can be authorized to a particular group.

## Casbin authorization policies

With Casbin, it is necessary to determine which resources exists and who can access to them. This are called **policies**.

In this example, there are policies already defined. They are contained in the test.db file (using sqlite3).

These are the defined policies:

| Type of policy (ptype) | Role (v0) | Resource/Resource Group (v1) | Action (v3)
| :---: | :---: | :---: | :---: |
| p | admin | data_group | read |
| p | admin | data_group | write |
| p | user | data_group | read |

The above tables shows that there are two roles: `admin` and `user`. Both have authorization to a group of resources called `data_group`. The `admin` role can read and `write` resources contained in the `data_group` and the `user` role can only `read`. 

The next table shows which resources belong to `data_group`:

| Type of policy (ptype) | Resource (v0) | Resource Group (v1) |
| :---: | :---: | :---: |
g2 | users | data_group |
g2 | activities | data_group |

There are two available resources (`users` and `activities`) contained in `data_group`.

All the previous policies are stored in 1 table in test.db database. The table is called `casbin_rule` and it is shown like this:

| ptype | v0 | v1 | v3 | v4 | v5
| :---: | :---: | :---: | :---: | :---: | :---: |
| p | admin | data_group | read | NULL | NULL
| p | admin | data_group | write | NULL | NULL
| p | user | data_group | read | NULL | NULL
g2 | users | data_group | NULL | NULL | NULL
g2 | activities | data_group | NULL | NULL | NULL

In conclusion, here is a summary of the described policies:
- An `admin` can `read` and `write` resources of `data_group`
- An `user` can only `read` resources of `data_group`
- There are two resources `users` and `activities` that belongs to `data_group`.

## Using PyCasbin

We created a decorator called `authorizator`. This decorator helps us to access to the `user` table that contains users and their roles.

Here are the available users:

| id | name | role
| :---: | :---: | :---: |
1 | Erick | admin
2 | Michael | admin
3 | Luis | admin

The decorator receives two params: `resource` and `action` and also gets a url param `userid` to get the information of an user, so it checks if an user (by its role) can do some `action` to a particular `resource`.

**For this decorator, it is necessary to determine the `resource` and `action` of each Flask API**

In the following example, it is determined that, for the API create_user, it will require a `write` authorization for the `users` resource.

```python
@app.route("/create/user")
@authorizator("users", "write")
def create_user():
    return f"<h3>You are allowed to make this requests: create_user()</h3>"
```

## URL tests

You can try these urls to test the authorization process using Casbin (you need to run the flask app first):

- [Erick (admin) trying to create user](http://localhost:5000/create/user?userid=1)
- [Luis (user) trying to create user](http://localhost:5000/create/user?userid=3)
- [Michael (admin) trying to get users](http://localhost:5000/users?userid=1)
- [Luis (user) trying to get users](http://localhost:5000/users?userid=3)

You can see more about PyCasbin documentation [here](https://github.com/casbin/pycasbin).

# Pros & Cons of Casbin/Casdoor

## Pros:

- Casdoor is developed in Go, but there are SDKs for other languages (python, JS).
- Casbin supports many sql database engines (mysql, postgres) (it supports only relational databases).
- Casbin is really useful for 
- A docker image for casbin/casdoor exists and can be configured.
- Casdoor's SDK will allow you to easily connect your application to the Casdoor authentication system without having to implement it from scratch.

## Cons:

- There aren’t many useful tutorials for Casdoor developments.
- A new database structure could be required for Casdoor implementation (new tables).
- Casbin does not do authentication.
- Casdoor is a third-party User-Role Management platform, so more resources may be required to implement it.
- There are no documentation for third party authentication providers such as Google for Casdoor
- Official demos are not working as expected with third party authentication such as Google and Facebook.
- ince Casdoor is a UI-based OAuth provider, you cannot use a request management service like Postman to send a URL with parameters and get back a JSON file.
- Most of its documentation is outdated.

