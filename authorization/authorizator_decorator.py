import casbin_sqlalchemy_adapter
import casbin
from flask import request

from utils import SQLITE_CONN, get_user_by_id
from utils.db_engine import SQLiteEngine

def authorizator(obj: str, act: str):
    def authorization(func):
        def wrapper():
            adapter = casbin_sqlalchemy_adapter.Adapter(SQLITE_CONN)
            e = casbin.Enforcer('./casbin_files/models/rbac_with_roles.conf', adapter)
            
            try:
                user_id = request.args.get('userid')
                user = get_user_by_id(SQLiteEngine(), user_id)
                sub = user[2]  # user role

                if e.enforce(sub, obj, act): # check if that user is authorized
                    response =  func()
                else:
                    response = f'<p>We\'re sorry {user[1]}, but as an {sub}, you don\'t have the authorization for {act} {obj}</p>'

                return f"{response}<br><br><p>Request by: {user[1]} ({user[2]})</p>"
            except Exception:
                return f'<p>User not found</p>'
        wrapper.__name__ = func.__name__
        return wrapper
    return authorization