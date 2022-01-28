import casbin_sqlalchemy_adapter
import casbin
from utils import SQLITE_CONN

"""
This is a test file, do not use it
"""

adapter = casbin_sqlalchemy_adapter.Adapter(SQLITE_CONN)
e = casbin.Enforcer('./casbin_files/models/rbac_with_roles.conf', adapter)
sub = "user"  # the user that wants to access a resource.
obj = "activities"  # the resource that is going to be accessed.
act = "write"  # the operation that the user performs on the resource.

if e.enforce(sub, obj, act):
    print('yes')
else:
    print('no')