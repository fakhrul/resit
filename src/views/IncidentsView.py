#/src/views/IncidentView.py
from flask import Flask, request, g, Blueprint, json, Response, send_file
from marshmallow import ValidationError, EXCLUDE
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.IncidentModel import IncidentModel, IncidentSchema
# from ..models.DashboardModel import DashboardSchema
from ..models.UserModel import UserModel
import os
import re
from ..shared.DatabaseManager import DatabaseManager
import datetime

app = Flask(__name__)
incident_api = Blueprint('incident_api', __name__)
incident_schema = IncidentSchema()
# dashboard_schema = DashboardSchema()
_database = DatabaseManager()

@incident_api.route('/', methods=['GET'])
# @Auth.auth_required
def get_all():
    posts = IncidentModel.get_all()
    data = incident_schema.dump(posts, many=True)
    return custom_response('success','',data, 200)


@incident_api.route('/by_date/<string:start>/<string:end>', methods=['GET'])
@Auth.auth_required
def get_all_by_date(start, end):
    start_object = datetime.datetime.strptime(start, '%Y%m%d%H%M%S')
    end_object = datetime.datetime.strptime(end, '%Y%m%d%H%M%S')

    posts = IncidentModel.get_all_by_date(start_object, end_object)
    data = incident_schema.dump(posts, many=True)

    return custom_response('success','',data, 200)

@incident_api.route('/latest10', methods=['GET'])
# @Auth.auth_required
def get_all_by_latest10():
    posts = IncidentModel.get_all_by_latest10()
    data = incident_schema.dump(posts, many=True)

    return custom_response('success','',data, 200)




@incident_api.route('/<int:incident_id>', methods=['GET'])
@Auth.auth_required
def get_one(incident_id):
    post = IncidentModel.get_one(incident_id)
    if not post:
        return custom_response('error','empty',{}, 404)
    data = incident_schema.dump(post)
    return custom_response('success','',data, 200)


# @incident_api.route('/dashboard/', methods=['GET'])
# # @Auth.auth_required
# def get_dashboard_info():
#     post =_database.get_summary_incident_drone_bymonth()
#     # data = json.dumps(post)
#     # data = data.replace("'\'","''")
#     # # data = dashboard_schema.dump(post,many=True)

#     # print(data)
#     return custom_response('success','',post, 200)

# @incident_api.route('/dashboard/graph', methods=['GET'])
# # @Auth.auth_required
# def get_dashboard_graph():
#     data_date =_database.get_summary_incident_drone_bymonth_by_column('date')
#     data_total =_database.get_summary_incident_drone_bymonth_by_column('total')

#     reformat_date = []
#     for date in data_date:
#         reformat_date.append(date[0])
#     reformat_total = []
#     for total in data_total:
#         reformat_total.append(total[0])

    # print(data_date)
    # print(data_total)
    # data = json.dumps(post)
    # data = data.replace("'\'","''")
    # # data = dashboard_schema.dump(post,many=True)
    data = {
        "date" : reformat_date,
        "total" : reformat_total
    }

    # print(data)
    return custom_response('success','',data, 200)



@incident_api.route('/image/<imagepath>', methods=['GET'])
# @Auth.auth_required
def get_image(imagepath):
    fullpath = os.getenv('WORK_FOLDER') + "/files/images/" + imagepath
    if os.path.exists(fullpath) == False:
        return custom_response('error','not found',{}, 400)
    return send_file(fullpath, mimetype='image/gif')

# @incident_api.route('/video/<videopath>', methods=['GET'])
# # @Auth.auth_required
# def get_video(videopath):
#     # fullpath = os.getenv('VIDEO_PATH') + videopath
#     fullpath = os.getenv('WORK_FOLDER') + "/files/videos/" + videopath
#     if os.path.exists(fullpath) == False:
#         return custom_response('error','not found',{}, 400)
#     return send_file(fullpath, mimetype='video/avi')

@incident_api.route('/image_display/<imagepath>', methods=['GET'])
# @Auth.auth_required
def get_image_display(imagepath):
    fullpath = os.getenv('WORK_FOLDER') + "/files/images_display/" + imagepath
    if os.path.exists(fullpath) == False:
        return custom_response('error','not found',{}, 400)

    return send_file(fullpath, mimetype='image/gif')

# @incident_api.route('/video_display/<videopath>', methods=['GET'])
# # @Auth.auth_required
# def get_video_display(videopath):
#     # fullpath = os.getenv('VIDEO_PATH') + videopath
#     fullpath = os.getenv('WORK_FOLDER') + "/files/videos_display/" + videopath
#     if os.path.exists(fullpath) == False:
#         return custom_response('error','not found',{}, 400)
#     return send_file(fullpath, mimetype='video/avi')

# @incident_api.route('/stream/<videopath>', methods=['GET'])
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


@incident_api.route('/', methods=['POST'])
# @Auth.auth_required
@Auth.auth_required
def create():
    req_data = request.get_json()
    # user = UserModel.get_one_user(g.user.get('id'))
    # req_data['owner_id'] = user.id
    print(req_data)

    try:
        data = incident_schema.load(req_data)
    except ValidationError as err:
        return custom_response('error',err,{}, 400)
        
    post = IncidentModel(data)
    post.save()
    data = incident_schema.dump(post)
    return custom_response('success','',data, 200)

@incident_api.route('/<int:incident_id>', methods=['PUT'])
# @Auth.auth_required
@Auth.auth_required
def update(incident_id):
    req_data = request.get_json()
    print(req_data)
    obj = IncidentModel.get_one(incident_id)
    if not obj:
        return custom_response('error','empty',{}, 404)
    print('foundObj', obj)
    # data = incident_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response('error','permission denied',data, 400)

    try:
        data = incident_schema.load(req_data, )
    except ValidationError as err:
        print('FOUND ERROR')
        return custom_response('error',err,{}, 400)

    obj.update(data)
    data = incident_schema.dump(obj)
    return custom_response('success','',data, 200)


@incident_api.route('/actualincident/<int:incident_id>', methods=['PUT'])
# @Auth.auth_required
@Auth.auth_required
def update_actual_incident(incident_id):
    req_data = request.get_json()
    obj = IncidentModel.get_one(incident_id)
    if not obj:
        return custom_response('error','empty',{}, 404)
    
    try:
        data = incident_schema.load(req_data, )
    except ValidationError as err:
        return custom_response('error',err,{}, 400)
    
    obj.update(data)

    data = incident_schema.dump(obj)
    return custom_response('success','',data, 200)



@incident_api.route('/<int:incident_id>', methods=['DELETE'])
# @Auth.auth_required
@Auth.auth_required
def delete(incident_id):
    post = IncidentModel.get_one(incident_id)
    if not post:
        return custom_response('error','hot found',{}, 400)
    data = incident_schema.dump(post)
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