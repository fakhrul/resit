#src/shared/Authentication
import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel


class Auth():
    """
    Auth Class
    """
    @staticmethod
    def generate_token(user_id):
        """
        Generate Token Method
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            result =  jwt.encode(
                payload,
                key=os.getenv('JWT_SECRET_KEY'),
                algorithm='HS256'
            )
            return result
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'error in generating user token: '+str(e)}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        """
        Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(
                jwt=token, 
                key=os.getenv('JWT_SECRET_KEY'),
                algorithms='HS256')
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again: '+str(e1)}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token, please try again with a new token'}
            return re

    #decorator
    @staticmethod
    def auth_required(func):
        """
        Auth decorator
        """
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'Api-Token' not in request.headers:

                return Auth.custom_response(
                    'error',
                    'Authentication token is not available, please login to get one',
                    {},
                    400
                )
                # return Response(
                #     mimetype="application/json",
                #     response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
                #     status=400
                # )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=401
                )
            
            user_id = data['data']['user_id']
            check_user = UserModel.get_one_user(user_id)
            if not check_user:
                return Response(
                  mimetype="application/json",
                  response=json.dumps({'error': 'user does not exist, invalid token'}),
                  status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs)
            
        return decorated_auth
    
    @staticmethod
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