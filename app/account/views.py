from flask import Blueprint, request, url_for, jsonify
from flask_restful import reqparse, Resource
from ..models import Users
from app import api, jwt, db
from flask_jwt_extended import create_access_token, jwt_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

accout = Blueprint('account', __name__)
parser = reqparse.RequestParser()
parser.add_argument('username', help='This parameter is required')
parser.add_argument('password', help='This parameter is required')


# @accout.route('/login')
class Login(Resource):
    def post(self):
        parser_arg = parser.parse_args()
        username = parser_arg['username']
        password = parser_arg['password']
        user = Users.query.filter_by(
            username=username, password=password).one_or_none()
        if not user:
            return jsonify("Error"), 401
        access = create_access_token(identity=user.to_json())
        print(user)
        return jsonify(acces_token=access)


class Register(Resource):
    def post(self):
        data = parser.parse_args()
        username = data['username'] or None
        password = data['password'] or None

        if None in [username, password] or not Users.query.filter_by(
                username=username).one_or_none():
            return jsonify(message='Has wrong')
        new = Users(username=username, password=generate_password_hash(password))
        db.session.add(new)
        db.session.commit()

        return jsonify(new_user=new.username)


@accout.route('/')
@jwt_required()
def hello():
    print(current_user.id)
    return 'Hello'


# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    print('11111111111111111111111', identity)
    user = Users.query.filter_by(id=identity['id']).one_or_none()
    return user


api.add_resource(Login, '/token')
api.add_resource(Register, '/register')


