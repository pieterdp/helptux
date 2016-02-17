from flask import render_template, redirect, url_for, abort
from helptux.views.blog.viewer import ViewPost
from helptux.modules.api.post import PostApi
from helptux.modules.error import DatabaseItemDoesNotExist
from helptux import app

a_post = PostApi()
v_post = ViewPost()


@app.route('/blog/<int:post_id>')
@app.route('/blog/post/<int:post_id>')
def v_show_post(post_id):
    # Get the existing post
    try:
        post = a_post.read(post_id)
    except DatabaseItemDoesNotExist as e:
        # Do a 404
        abort(404)
        return ''
    if post.is_deleted:
        abort(404)
        return ''
    if not post.is_visible:
        abort(404)
        return ''
    display_post = v_post.post_to_output_obj(post)
    return render_template('public/post.html', post=display_post)


@app.route('/blog/tag/<int:tag_id>')
def v_show_tag(tag_id):
    return ''
