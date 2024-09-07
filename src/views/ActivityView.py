#/src/views/ActivityView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.ActivityModel import ActivityModel, ActivitySchema
from ..models.UserModel import UserModel

app = Flask(__name__)
activity_api = Blueprint('activity_api', __name__)
activity_schema = ActivitySchema()


@activity_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Activitys
    """
    posts = ActivityModel.get_all()
    data = activity_schema.dump(posts, many=True)
    return custom_response(data, 200)

@activity_api.route('/<int:activity_id>', methods=['GET'])
def get_one(activity_id):
    """
    Get A Activity
    """
    post = ActivityModel.get_one(activity_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = activity_schema.dump(post)
    return custom_response(data, 200)
    
@activity_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Activity Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = activity_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)
        
    post = ActivityModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = activity_schema.dump(post)
    return custom_response(data, 201)    

@activity_api.route('/<int:activity_id>', methods=['PUT'])
@Auth.auth_required
def update(activity_id):
    """
    Update A Activity
    """
    req_data = request.get_json()
    post = ActivityModel.get_one(activity_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = activity_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = activity_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = activity_schema.dump(post)
    return custom_response(data, 200)

@activity_api.route('/<int:activity_id>', methods=['DELETE'])
@Auth.auth_required
def delete(activity_id):
    """
    Delete A Activity
    """
    post = ActivityModel.get_one(activity_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = activity_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    post.delete()
    return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )