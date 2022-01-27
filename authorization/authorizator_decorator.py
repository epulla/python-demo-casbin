import casbin_sqlalchemy_adapter
import casbin

def authorizator(obj: str, act: str):
    def authorization(func):
        def wrapper():
            adapter = casbin_sqlalchemy_adapter.Adapter('sqlite:///test.db')
            e = casbin.Enforcer('./casbin_files/models/rbac_with_roles.conf', adapter)
            sub = "admin"  # the user that wants to access a resource.
            obj = "activities"  # the resource that is going to be accessed.
            act = "read"  # the operation that the user performs on the resource.

            if e.enforce(sub, obj, act):
                func()
            else:
                return f'<p>As an {sub}, you don\'t have the authorization for {act} {obj}</p>'
        
        return wrapper
    return authorization