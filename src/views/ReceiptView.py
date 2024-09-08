from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.ReceiptModel import ReceiptModel, ReceiptSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
receipt_api = Blueprint('receipt_api', __name__)
receipt_schema = ReceiptSchema()


@receipt_api.route('/', methods=['GET'])
def get_all():
    posts = ReceiptModel.get_all()
    data = receipt_schema.dump(posts, many=True)
    return custom_response(data, 200)

@receipt_api.route('/<int:receipt_id>', methods=['GET'])
def get_one(receipt_id):
    post = ReceiptModel.get_one(receipt_id)
    if not post:
        return custom_response({'error': 'Receipt not found'}, 404)
    data = receipt_schema.dump(post)
    return custom_response(data, 200)

@receipt_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    app.logger.info('Received data for creating receipt: ' + json.dumps(req_data))
    
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['user_id'] = user.id  # Use consistent naming: `user_id` instead of `owner_id`

    try:
        data = receipt_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err.messages, 400)
    
    post = ReceiptModel(data)
    post.save()

    try:
        app.logger.info('Sending email notification...')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)

    data = receipt_schema.dump(post)
    return custom_response(data, 201)

@receipt_api.route('/<int:receipt_id>', methods=['PUT'])
@Auth.auth_required
def update(receipt_id):
    req_data = request.get_json()
    post = ReceiptModel.get_one(receipt_id)
    if not post:
        return custom_response({'error': 'Receipt not found'}, 404)
    
    # Check ownership directly from model, no need to dump
    if post.user_id != g.user.get('id'):
        return custom_response({'error': 'Permission denied'}, 403)

    try:
        data = receipt_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err.messages, 400)

    post.update(data)
    data = receipt_schema.dump(post)
    return custom_response(data, 200)

@receipt_api.route('/<int:receipt_id>', methods=['DELETE'])
@Auth.auth_required
def delete(receipt_id):
    post = ReceiptModel.get_one(receipt_id)
    if not post:
        return custom_response({'error': 'Receipt not found'}, 404)

    if post.user_id != g.user.get('id'):
        return custom_response({'error': 'Permission denied'}, 403)

    post.delete()
    return custom_response({'message': 'Receipt deleted'}, 204)


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
