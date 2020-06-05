from flask_restful import Resource
from flask import request, jsonify
from flask_http_response import result, error
from flask_jwt_extended import jwt_required

from main import db
from ..models.user import User
from ..schemas.user import UserSchema


class UserListView(Resource):
    decorators = [jwt_required]

    def get(self):
        page = request.args.get('page', 1)
        page_size = request.args.get('page_size', 10)
        users = User.query.filter_by()

        paginated_data = users.order_by(User.id.desc()).paginate(page, page_size, error_out=False)
        response = UserSchema(many=True).dump(paginated_data.items)
        payload = {
            'current_page': paginated_data.page,
            'page_size': paginated_data.per_page,
            'total_count': paginated_data.total,
            'results': response
        }
        return result.return_response(payload)


class UserPostView(Resource):
    
    def post(self):
        request_data = request.get_json()
        user = User.query.filter_by(email=request_data.get('email')).first()

        if user:
            return error.return_response('User already exists')
        
        user = User(**request_data)
        db.session.add(user)
        db.session.commit()
        db.session.flush()
        response = UserSchema().dump(user)
        return result.return_response(response, 201) 