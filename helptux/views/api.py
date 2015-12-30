from flask import request
import json
from helptux.modules.api import HelptuxApi
from helptux.modules.api.post import PostApi
from helptux.modules.api.tag import TagApi
from helptux.modules.api.type import TypeApi
from helptux.modules.api.category import CategoryApi
from helptux import app


@app.route('/api/post/<int:post_id>', methods=['GET', 'DELETE'])
@app.route('/api/author/<int:author_id>/type/<int:type_id>/post', methods=['POST'])
@app.route('/api/author/<int:author_id>/type/<int:type_id>/post/<int:post_id>', methods=['PUT'])
def a_post(author_id=None, type_id=None, post_id=None):
    a_api = HelptuxApi(api_class=PostApi)
    out_data = u''
    if request.method == 'GET':
        out_data = a_api.read(post_id)
    else:
        input_data_raw = request.get_data()
        input_data_dict = json.loads(input_data_raw.decode('utf-8'))
        if request.method == 'POST':
            out_data = a_api.create(input_data_dict, {'type_id': type_id, 'author_id': author_id})
        if request.method == 'PUT':
            out_data = a_api.update(post_id, input_data_dict, {'type_id': type_id, 'author_id': author_id})
        if request.method == 'DELETE':
            out_data = a_api.delete(post_id)
    return a_api.response(out_data)


@app.route('/api/tag/<int:tag_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/tag', methods=['POST'])
def a_tag(tag_id=None):
    pass


@app.route('/api/type/<int:type_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/type', methods=['POST'])
def a_type(type_id=None):
    pass


@app.route('/api/author/<int:author_id>', methods=['GET'])
def a_author(author_id):
    pass
