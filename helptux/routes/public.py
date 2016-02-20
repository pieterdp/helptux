from flask import render_template, redirect, url_for, abort, flash
from helptux.views.blog.viewer import ViewPost
from helptux.modules.api.post import PostApi
from helptux.modules.error import DatabaseItemDoesNotExist
from helptux import app

a_post = PostApi()
v_post = ViewPost()


@app.route('/blog/post/<int:post_id>')
@app.route('/blog/<int:post_id>')
@app.route('/blog/post/<string:post_slug>')
@app.route('/blog/<string:post_slug>')  # Strings are default, get them last (ints are also strings)
def v_show_post(post_id=None, post_slug=None):
    # Get the existing post
    try:
        if post_id:
            post = a_post.read(post_id)
        elif post_slug:
            post = a_post.by_slug(post_slug)
        else:
            raise DatabaseItemDoesNotExist
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
    return render_template('public/post.html', post=display_post,
                           extra_css=['bower_components/bootstrap/dist/css/bootstrap-blog.css'])


@app.route('/blog/post')
@app.route('/post')
@app.route('/blog/post/')
@app.route('/post/')
@app.route('/blog/p/<int:page>')
@app.route('/blog/post/p/<int:page>')
def v_list_post(page=None):
    # Get the list for this page
    try:
        post_list = a_post.paginate(page)
    except DatabaseItemDoesNotExist as e:
        flash('No more pages.')
        return redirect(url_for('.v_index'))
    next_page = post_list.next(error_out=False)
    previous_page = post_list.prev(error_out=False)
    display_posts = []
    for post in post_list.items:
        print(post.id)
        display_posts.append(v_post.post_to_output_obj(post))
    return render_template('public/list.html', posts=display_posts, next=next_page, previous=previous_page,
                           extra_css=['bower_components/bootstrap/dist/css/bootstrap-blog.css'], title='Posts')


@app.route('/blog/tag/<int:tag_id>')
@app.route('/blog/tag/<string:tag>')
def v_show_tag(tag_id=None, tag=None):
    return ''


@app.route('/blog/tag')
@app.route('/blog/tag/')
def v_list_tag():
    return ''


@app.route('/<string:page_slug>')
@app.route('/page/<string:page_slug>')
def v_show_page(page_slug):
    try:
        page = a_post.by_slug(page_slug)
    except DatabaseItemDoesNotExist as e:
        abort(404)
        return ''
    if page.type.type != 'page':
        abort(404)
        return ''
    if page.is_deleted:
        abort(404)
        return ''
    if not page.is_visible:
        abort(404)
        return ''
    display_page = v_post.post_to_output_obj(page)
    return render_template('public/page.html', page=display_page, title=display_page['title'])
