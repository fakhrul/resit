#/src/views/UserView

import datetime
from flask import Flask, request, json, Response, Blueprint, g, jsonify
from marshmallow import ValidationError
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth
from ..models.EventModel import EventModel, EventSchema
import base64

app = Flask(__name__)
user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()
event_schema = EventSchema()

@user_api.route('/register', methods=['POST'])
def create():
    req_data = request.get_json()
    try:
        data = user_schema.load(req_data)
    except ValidationError as err:
        return custom_response('error',err,{}, 400)

    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        return custom_response('error','User already exist, please supply another email address',{}, 400)

    user = UserModel(data)
    user.save()

    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data.get('id'))
    return custom_response('success','',{'jwt_token': token}, 201)

# @user_api.route('/', methods=['GET'])
# @Auth.auth_required
# def get_all():
#     users = UserModel.get_all_users()
#     ser_users = user_schema.dump(users, many=True)
#     return custom_response(ser_users, 200)

@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    try:
        data = user_schema.load(req_data, partial=True)
    except ValidationError as err:
        print("dsdsd")
        return custom_response('error',err,{}, 400)

    if not data.get('email') or not data.get('password'):
        return custom_response('error',
                               'you need email and password to sign in',
                               {}, 400)

    user = UserModel.get_user_by_email(data.get('email'))
    if not user:
        return custom_response('error', 'User not found',{}, 400)
    if not user.check_hash(data.get('password')):
        return custom_response('error', 'Wrong Password', {},400)


    try:
        event_data_json = {
            "datetime" : datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "source" : "dds_web_admin",
            "eventtype" : "Activity",
            "info" : 'Login System',
            "details" : data.get('email'),
        }
        event_data = event_schema.load(event_data_json)
        eventModel = EventModel(event_data)
        eventModel.save()
        event_data = event_schema.dump(eventModel)

    except Exception as e:
        print('Error create event', e)
        pass


    ser_data = user_schema.dump(user)
    user_info = {
        'name' : str(ser_data.get('name'))
    }
    token = Auth.generate_token(ser_data.get('id'))
    token_string = ""
    if isinstance(token, (bytes, bytearray)):
        token_string = token.decode('utf-8')
    elif isinstance(token, str):
        token_string = token
    else:
        token_string = str(token)
    data = {
        # 'token':  token,
        'token': token_string,
        'user': ser_data,
        'status': 'success'
    }
    return custom_response('success','',data, 200)

@user_api.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('api-token')
    decode_token = token.encode('utf-8')
    data = Auth.decode_token(token)
    user_id = data['data']['user_id']
    check_user = UserModel.get_one_user(user_id)
    data = user_schema.dump(check_user)


    try:
        event_data_json = {
            "datetime" : datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "source" : "dds_web_admin",
            "eventtype" : "Activity",
            "info" : 'Logout System',
            "details" : data['email'],
        }
        event_data = event_schema.load(event_data_json)
        eventModel = EventModel(event_data)
        eventModel.save()
        event_data = event_schema.dump(eventModel)

    except Exception as e:
        print('Error create event', e)
        pass

    return custom_response('success','',{}, 200)
    # token = request.headers.get('api-token')
    # data = Auth.decode_token(token)    
# @user_api.route('/loginfg', methods=['POST'])
# def loginfg():
#     """
#     User Login Function
#     """
#     req_data = request.get_json()
#     app.logger.info('llega siquiera --------------#'+json.dumps(req_data))
    
#     try:
#         data = user_schema.load(req_data, partial=True)
#     except ValidationError as err:
#         return custom_response(err, 400)

#     if not data.get('email') or not data.get('tokenfg'):
#         return custom_response({'error': 'you need email and token from facebook/gmail to sign in'}, 400)

#     user = UserModel.get_user_by_email(data.get('email'))
#     if not user:
#         return custom_response({'error': 'email does not exist'}, 400)
#     # if not user.check_hash(data.get('password')):
#     #     return custom_response({'error': 'invalid credentials'}, 400)
#     #Aqui en vez de revisar password revisamos contra feis y google q si funcione el token válido

#     ser_data = user_schema.dump(user)

#     token = Auth.generate_token(ser_data.get('id'))

#     return custom_response({'jwt_token': token}, 200)  

@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)

    ser_user = user_schema.dump(user)
    return custom_response('success','',ser_user, 200)




# @user_api.route('/update_me', methods=['PUT'])
# # @Auth.auth_required
# def update_me():
#     # print(g.user.get('id'))
#     req_data = request.get_json()
#     return custom_response('success','',req_data, 200)

@user_api.route('/update_me', methods=['PUT'])
@Auth.auth_required
def update_me():
    req_data = request.get_json()

    user = UserModel.get_one_user(g.user.get('id'))
    if not user:
        return custom_response('error','empty',{}, 404)

    try:
        data = user_schema.load(req_data)
    except ValidationError as err:
        return custom_response('error',err,{}, 400)

    user.update(data)
    data = user_schema.dump(user)

    return custom_response('success','',data, 200)

# @user_api.route('/me', methods=['DELETE'])
# @Auth.auth_required
# def delete():
#     """
#     Delete a user
#     """
#     user = UserModel.get_one_user(g.user.get('id'))
#     user.delete()
#     return custom_response({'message': 'deleted'}, 204)

@user_api.route('/me/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_me(user_id):
    user = UserModel.get_one_user(user_id)
    data = user_schema.dump(user)
    return custom_response('success','',data, 200)


@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    posts = UserModel.get_all_users()
    data = user_schema.dump(posts, many=True)
    return custom_response('success','',data, 200)

@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_one(user_id):
    post = UserModel.get_one_user(user_id)
    if not post:
        return custom_response('error','empty',{}, 404)
    data = user_schema.dump(post)
    return custom_response('success','',data, 200)

# @user_api.route('/', methods=['POST'])
# # @Auth.auth_required
# def create():
#     req_data = request.get_json()
#     # user = UserModel.get_one_user(g.user.get('id'))
#     # req_data['owner_id'] = user.id
#     print(req_data)

#     try:
#         data = user_schema.load(req_data)
#     except ValidationError as err:
#         return custom_response('error',err,{}, 400)
        
#     post = UserModel(data)
#     post.save()
#     data = user_schema.dump(post)
#     return custom_response('success','',data, 200)

@user_api.route('/<int:user_id>', methods=['PUT'])
# @Auth.auth_required
@Auth.auth_required
def update(user_id):
    req_data = request.get_json()
    obj = UserModel.get_one_user(user_id)
    if not obj:
        return custom_response('error','empty',{}, 404)
    # print('foundObj', obj)
    # data = user_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response('error','permission denied',data, 400)

    try:
        data = user_schema.load(req_data, )
    except ValidationError as err:
        print('FOUND ERROR')
        return custom_response('error',err,{}, 400)

    obj.update(data)
    data = user_schema.dump(obj)
    return custom_response('success','',data, 200)

@user_api.route('/<int:user_id>', methods=['DELETE'])
# @Auth.auth_required
@Auth.auth_required
def delete(user_id):
    post = UserModel.get_one_user(user_id)
    if not post:
        return custom_response('error','not found',{}, 400)
    data = user_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    post.delete()
    return custom_response('success','',data, 200)



def custom_response(status, errorMsg, data, status_code):
    """
    Custom Response Function
    """
    info = {'status': status, 
            'errorMsg': errorMsg,
            'data':data}

    response = Response(
        mimetype="application/json",
        response=json.dumps(info),
        status=status_code
    )

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# def custom_response(res, status_code):
#     """
#     Custom Response Function
#     """
#     return Response(
#         mimetype="application/json",
#         response=json.dumps(res),
#         status=status_code
#     )
