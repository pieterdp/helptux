from flask import request, g
from flask.ext.login import login_required, current_user
import json

from helptux.modules.api import HelptuxApi
from helptux.modules.api.post import PostApi
from helptux.modules.api.tag import TagApi
from helptux.modules.api.type import TypeApi
from helptux.modules.api.category import CategoryApi
from helptux.modules.user.authentication import role_required, must_be_admin, must_be_editor, must_be_registered
from helptux import app


@app.route('/api/post/<int:post_id>', methods=['DELETE', 'PUT'])
@app.route('/api/post', methods=['POST'])
@login_required
@must_be_editor
def a_post(post_id=None):
    a_api = HelptuxApi(api_class=PostApi, o_request=request, api_obj_id=post_id,
                       additional_opts={'author_id': current_user.id})
    return a_api.response


@app.route('/api/post/<int:post_id>', methods=['GET'])
@app.route('/api/post', methods=['GET'])
def a_post_get(post_id=None):
    a_api = HelptuxApi(api_class=PostApi, o_request=request, api_obj_id=post_id)
    return a_api.response


@app.route('/api/tag/<int:tag_id>', methods=['PUT', 'DELETE'])
@app.route('/api/tag', methods=['POST'])
@login_required
@must_be_editor
def a_tag(tag_id=None):
    a_api = HelptuxApi(api_class=TagApi, o_request=request, api_obj_id=tag_id)
    return a_api.response


@app.route('/api/tag/<int:tag_id>', methods=['GET'])
@app.route('/api/tag', methods=['GET'])
def a_tag_get(tag_id=None):
    a_api = HelptuxApi(api_class=TagApi, o_request=request, api_obj_id=tag_id)
    return a_api.response


@app.route('/api/type/<int:type_id>', methods=['PUT', 'DELETE'])
@app.route('/api/type', methods=['POST'])
@login_required
@must_be_editor
def a_type(type_id=None):
    a_api = HelptuxApi(api_class=TypeApi, o_request=request, api_obj_id=type_id)
    return a_api.response


@app.route('/api/type/<int:type_id>', methods=['GET'])
@app.route('/api/type', methods=['GET'])
def a_type_get(type_id=None):
    a_api = HelptuxApi(api_class=TypeApi, o_request=request, api_obj_id=type_id)
    return a_api.response


@app.route('/api/category/<int:cat_id>', methods=['PUT', 'DELETE'])
@app.route('/api/category', methods=['POST'])
@login_required
@must_be_editor
def a_cat(cat_id=None):
    a_api = HelptuxApi(api_class=CategoryApi, o_request=request, api_obj_id=cat_id)
    return a_api.response


@app.route('/api/category/<int:cat_id>', methods=['GET'])
@app.route('/api/category', methods=['GET'])
def a_cat_get(cat_id=None):
    a_api = HelptuxApi(api_class=CategoryApi, o_request=request, api_obj_id=cat_id)
    return a_api.response


@app.route('/api/author/<int:author_id>', methods=['GET'])
def a_author(author_id):
    pass
