#/src/views/EventView.py
from flask import Flask, request, g, Blueprint, json, Response, send_file
from marshmallow import ValidationError, EXCLUDE
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.EventModel import EventModel, EventSchema
from ..models.UserModel import UserModel
import os
import re
import datetime

app = Flask(__name__)
event_api = Blueprint('event_api', __name__)
event_schema = EventSchema()


@event_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    """
    Get All Activitys
    """
    posts = EventModel.get_all()
    data = event_schema.dump(posts, many=True)
    return custom_response('success','',data, 200)

@event_api.route('/by_date/<string:start>/<string:end>', methods=['GET'])
@Auth.auth_required
def get_all_by_date(start, end):
    start_object = datetime.datetime.strptime(start, '%Y%m%d%H%M%S')
    end_object = datetime.datetime.strptime(end, '%Y%m%d%H%M%S')

    posts = EventModel.get_all_by_date(start_object, end_object)
    data = event_schema.dump(posts, many=True)

    return custom_response('success','',data, 200)


@event_api.route('/<int:event_id>', methods=['GET'])
@Auth.auth_required
def get_one(event_id):
    post = EventModel.get_one(event_id)
    if not post:
        return custom_response('error','empty',{}, 404)
    data = event_schema.dump(post)
    return custom_response('success','',data, 200)

@event_api.route('/image/<imagepath>', methods=['GET'])
@Auth.auth_required
def get_image(imagepath):
    print(imagepath)
    fullpath = os.getenv('WORK_FOLDER') + "/files/images/" + imagepath
    print(fullpath)
    return send_file(fullpath, mimetype='image/gif')

@event_api.route('/video/<videopath>', methods=['GET'])
@Auth.auth_required
def get_video(videopath):
    fullpath =os.getenv('WORK_FOLDER') + "/files/videos/"  + videopath
    print(fullpath)
    return send_file(fullpath, mimetype='video/avi')


# @event_api.route('/stream/<videopath>', methods=['GET'])
# def get_video_stream(videopath):
#     range_header = request.headers.get('Range', None)
#     byte1, byte2 = 0, None
#     if range_header:
#         match = re.search(r'(\d+)-(\d*)', range_header)
#         groups = match.groups()

#         if groups[0]:
#             byte1 = int(groups[0])
#         if groups[1]:
#             byte2 = int(groups[1])
       
#     chunk, start, length, file_size = get_chunk(videopath, byte1, byte2)
#     resp = Response(chunk, 206, mimetype='video/mp4',
#                       content_type='video/mp4', direct_passthrough=True)
#     resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
#     return resp
    
#     fullpath = os.getenv('VIDEO_PATH') + videopath
#     print(fullpath)
#     return send_file(fullpath, mimetype='video/avi')


# def get_chunk(videopath, byte1=None, byte2=None):
#     full_path = os.getenv('VIDEO_PATH') + videopath
#     file_size = os.stat(full_path).st_size
#     start = 0
    
#     if byte1 < file_size:
#         start = byte1
#     if byte2:
#         length = byte2 + 1 - byte1
#     else:
#         length = file_size - start

#     with open(full_path, 'rb') as f:
#         f.seek(start)
#         chunk = f.read(length)
#     return chunk, start, length, file_size


@event_api.route('/', methods=['POST'])
# @Auth.auth_required
@Auth.auth_required
def create():
    req_data = request.get_json()
    # user = UserModel.get_one_user(g.user.get('id'))
    # req_data['owner_id'] = user.id
    print(req_data)

    try:
        data = event_schema.load(req_data)
    except ValidationError as err:
        return custom_response('error',err,{}, 400)
        
    post = EventModel(data)
    post.save()
    data = event_schema.dump(post)
    return custom_response('success','',data, 200)

@event_api.route('/<int:event_id>', methods=['PUT'])
# @Auth.auth_required
@Auth.auth_required
def update(event_id):
    req_data = request.get_json()
    print(req_data)
    obj = EventModel.get_one(event_id)
    if not obj:
        return custom_response('error','empty',{}, 404)
    print('foundObj', obj)
    # data = event_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response('error','permission denied',data, 400)

    try:
        data = event_schema.load(req_data, )
    except ValidationError as err:
        print('FOUND ERROR')
        return custom_response('error',err,{}, 400)

    obj.update(data)
    data = event_schema.dump(obj)
    return custom_response('success','',data, 200)

@event_api.route('/<int:event_id>', methods=['DELETE'])
# @Auth.auth_required
@Auth.auth_required
def delete(event_id):
    post = EventModel.get_one(event_id)
    if not post:
        return custom_response('error','hot found',{}, 400)
    data = event_schema.dump(post)
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