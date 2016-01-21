from flask import render_template, url_for, flash, request, redirect
from flask.ext.login import login_required
from helptux.modules.api.post import PostApi
from helptux.modules.user.authentication import must_be_editor
from helptux import app


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
    pass
