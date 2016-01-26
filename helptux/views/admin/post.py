from flask import render_template, url_for, flash, request, redirect
from flask.ext.login import login_required
from helptux.modules.api.post import PostApi
from helptux.modules.api.type import TypeApi
from helptux.modules.user.authentication import must_be_editor
from helptux.views.forms.post.admin import PostCreateForm
from helptux import app


a_type = TypeApi()
db_types = a_type.list()
possible_types = []
for db_type in db_types:
    possible_types.append((db_type.id, db_type.type))


@app.route('/admin/post/list', methods=['GET'])
@login_required
@must_be_editor
def v_post_list():
    a_post = PostApi()
    l_posts = a_post.list()
    return render_template('admin/post/list.html', posts=l_posts)


@app.route('/admin/post/create', methods=['GET', 'POST'])
@login_required
@must_be_editor
def v_post_create():
    # Store the tags like if match then foo, else bar
    # input type=text; onlosefocus => use api to store them, onsubmit link (?)
    return render_template('admin/post/create.html', post_id=-1)


@app.route('/admin/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@must_be_editor
def v_post_edit(post_id):
    return render_template('admin/post/edit.html', post_id=post_id)


@app.route('/admin/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
@must_be_editor
def v_post_delete(post_id):
    pass
