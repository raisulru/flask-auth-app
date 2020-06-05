from flask_restful import Resource
from flask import request, jsonify
from flask_http_response import result, error
from flask_jwt_extended import create_access_token

from ..models.user import User


class LoginView(Resource):

    def check_user_id_and_password(self, username, password):
        user = User.query.filter_by(email=username).first()

        if not user:
            return
        
        if user.password != password:
            return
        return user


    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return error.return_response("Missing username parameter")
        
        if not password:
            return error.return_response("Missing password parameter")

        if not self.check_user_id_and_password(username, password):
            return error.return_response("Bad username or password", 401)

        access_token = create_access_token(identity=username)
        payload = {
            'access_token': access_token
        }
        return result.return_response(payload, 201)