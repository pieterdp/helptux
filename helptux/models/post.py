from helptux import db
from datetime import datetime
from time import time
import pytz
import re
# TODO is_deleted, is_visible


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255), index=True, nullable=False, unique=True)

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return u'<Tag {0}>'.format(self.tag)

    def output_obj(self):
        return {
            'id': self.id,
            'tag': self.tag,
            'posts': [p.id for p in self.posts]
        }


tags_posts = db.Table('tags_posts',
                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                      db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
                      )


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), index=True, nullable=False)
    slug = db.Column(db.String(32), index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    creation_time = db.Column(db.DateTime, default=None)
    last_modified = db.Column(db.DateTime, default=None)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag',
                           secondary=tags_posts,
                           primaryjoin=(tags_posts.c.post_id == id),
                           secondaryjoin=(tags_posts.c.tag_id == Tag.id),
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')

    def __init__(self, title, content, creation_time=None, last_modified=None, is_visible=None, is_deleted=None):
        self.title = title
        self.slug = self.mk_slug(title)
        self.content = content
        if creation_time is None:
            self.creation_time = datetime.now(tz=pytz.timezone('Europe/Brussels'))
        else:
            self.creation_time = creation_time
        if last_modified is None:
            self.last_modified = datetime.now(tz=pytz.timezone('Europe/Brussels'))
        else:
            self.last_modified = last_modified
        self.is_deleted = is_deleted
        self.is_visible = is_visible

    def __repr__(self):
        return '<Post {0}>'.format(self.title)

    def output_obj(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'abstract': self.abstract,
            'creation_time': self.creation_time.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'is_visible': self.is_visible,
            'is_deleted': self.is_deleted,
            'type_id': self.type_id,
            'author_id': self.author_id,
            'tags': [t.output_obj() for t in self.tags]
        }

    @property
    def abstract(self):
        return self.content[:100]

    def mk_slug(self, title):
        # [^a-z]
        # to lower
        # sub
        # A slug is like [chars from the original title]-[timestamp] and is 32 characters
        non_alpha = re.compile('[^a-z]')
        max_or_part_length = 32 - len(str(round(time())))
        s_title = title.lower()
        s_title = s_title[:max_or_part_length]
        proposed_slug = non_alpha.sub('-', s_title)
        # Check whether it exists, if it does, add the time. If it doesn't, just use it, as it is prettier
        post_exists = Post.query.filter(Post.slug == proposed_slug).first()
        if post_exists:
            return '{0}-{1}'.format(proposed_slug, str(round(time())))
        else:
            return '{0}'.format(proposed_slug)


class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), index=True, unique=True, nullable=False)
    posts = db.relationship('Post', backref='type', lazy='dynamic')

    def __init__(self, s_type):
        self.type = s_type

    def __repr__(self):
        return '<Type {0}>'.format(self.type)

    def output_obj(self):
        return {
            'id': self.id,
            'type': self.type,
            'posts': [p.id for p in self.posts]
        }
