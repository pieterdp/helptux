from flask import request
import json

from helptux.modules.api import HelptuxApi
from helptux.modules.api.post import PostApi
from helptux.modules.api.tag import TagApi
from helptux.modules.api.type import TypeApi
from helptux.modules.api.category import CategoryApi
from helptux import app


@app.route('/api/post/<int:post_id>', methods=['GET', 'DELETE', 'PUT'])
@app.route('/api/post', methods=['POST'])
def a_post(author_id=None, type_id=None, post_id=None):
    a_api = HelptuxApi(api_class=PostApi)
    out_data = u''
    if request.method == 'GET':
        # TODO: if is_visible is False: require_auth
        # TODO: if is_deleted is False: require_auth
        out_data = a_api.read(post_id)
    elif request.method == 'DELETE':
        out_data = a_api.delete(post_id)
    else:
        input_data_raw = request.get_data()
        input_data_string = input_data_raw.decode('utf-8')
        try:
            input_data_dict = json.loads(input_data_string)
        except ValueError as e:
            a_api.msg = u'A JSON error occurred: {0}'.format(e)
        else:
            if request.method == 'POST':
                out_data = a_api.create(input_data_dict, {})
            if request.method == 'PUT':
                out_data = a_api.update(post_id, input_data_dict, {})
    return a_api.response(out_data)


@app.route('/api/tag/<int:tag_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/tag', methods=['POST'])
def a_tag(tag_id=None):
    a_api = HelptuxApi(api_class=TagApi)
    out_data = u''
    if request.method == 'GET':
        out_data = a_api.read(tag_id)
    elif request.method == 'DELETE':
        out_data = a_api.delete(tag_id)
    else:
        input_data_raw = request.get_data()
        input_data_string = input_data_raw.decode('utf-8')
        try:
            input_data_dict = json.loads(input_data_string)
        except ValueError as e:
            a_api.msg = u'A JSON error occurred: {0}'.format(e)
        else:
            if request.method == 'POST':
                out_data = a_api.create(input_data_dict, {})
            if request.method == 'PUT':
                out_data = a_api.update(tag_id, input_data_dict, {})
    return a_api.response(out_data)


@app.route('/api/type/<int:type_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/type', methods=['POST'])
def a_type(type_id=None):
    a_api = HelptuxApi(api_class=TypeApi)
    out_data = u''
    if request.method == 'GET':
        out_data = a_api.read(type_id)
    elif request.method == 'DELETE':
        out_data = a_api.delete(type_id)
    else:
        input_data_raw = request.get_data()
        input_data_string = input_data_raw.decode('utf-8')
        try:
            input_data_dict = json.loads(input_data_string)
        except ValueError as e:
            a_api.msg = u'A JSON error occurred: {0}'.format(e)
        else:
            if request.method == 'POST':
                out_data = a_api.create(input_data_dict, {})
            if request.method == 'PUT':
                out_data = a_api.update(type_id, input_data_dict, {})
    return a_api.response(out_data)


@app.route('/api/category/<int:cat_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/category', methods=['POST'])
def a_cat(cat_id=None):
    a_api = HelptuxApi(api_class=CategoryApi)
    out_data = u''
    if request.method == 'GET':
        out_data = a_api.read(cat_id)
    elif request.method == 'DELETE':
        out_data = a_api.delete(cat_id)
    else:
        input_data_raw = request.get_data()
        input_data_string = input_data_raw.decode('utf-8')
        try:
            input_data_dict = json.loads(input_data_string)
        except ValueError as e:
            a_api.msg = u'A JSON error occurred: {0}'.format(e)
        else:
            if request.method == 'POST':
                out_data = a_api.create(input_data_dict, {})
            if request.method == 'PUT':
                out_data = a_api.update(cat_id, input_data_dict, {})
    return a_api.response(out_data)


@app.route('/api/author/<int:author_id>', methods=['GET'])
def a_author(author_id):
    pass
