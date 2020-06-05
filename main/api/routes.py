from ..api import api
from ..views import *

api.add_resource(StatusView, '/status')
api.add_resource(UserListView, '/users')
api.add_resource(UserPostView, '/registration')
api.add_resource(LoginView, '/login')
