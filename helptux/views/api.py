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
def a_post(post_id=None):
    a_api = HelptuxApi(api_class=PostApi, o_request=request, api_obj_id=post_id)
    return a_api.response


@app.route('/api/tag/<int:tag_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/tag', methods=['POST'])
def a_tag(tag_id=None):
    a_api = HelptuxApi(api_class=TagApi, o_request=request, api_obj_id=tag_id)
    return a_api.response


@app.route('/api/type/<int:type_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/type', methods=['POST'])
def a_type(type_id=None):
    a_api = HelptuxApi(api_class=TypeApi, o_request=request, api_obj_id=type_id)
    return a_api.response


@app.route('/api/category/<int:cat_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/category', methods=['POST'])
def a_cat(cat_id=None):
    a_api = HelptuxApi(api_class=CategoryApi, o_request=request, api_obj_id=cat_id)
    return a_api.response


@app.route('/api/author/<int:author_id>', methods=['GET'])
def a_author(author_id):
    pass
