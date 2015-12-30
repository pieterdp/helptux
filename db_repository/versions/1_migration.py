from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
categories = Table('categories', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('category', String(length=255), nullable=False),
)

categories_posts = Table('categories_posts', post_meta,
    Column('category_id', Integer),
    Column('post_id', Integer),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=512), nullable=False),
    Column('content', Text, nullable=False),
    Column('creation_time', DateTime, nullable=False),
    Column('last_modified', DateTime, nullable=False),
    Column('is_visible', Boolean, nullable=False, default=ColumnDefault(True)),
    Column('is_deleted', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('type_id', Integer),
    Column('author_id', Integer),
)

tags = Table('tags', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tag', String(length=255), nullable=False),
)

tags_posts = Table('tags_posts', post_meta,
    Column('tag_id', Integer),
    Column('post_id', Integer),
)

types = Table('types', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=255), nullable=False),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=255), nullable=False),
    Column('email', String(length=255), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['categories'].create()
    post_meta.tables['categories_posts'].create()
    post_meta.tables['posts'].create()
    post_meta.tables['tags'].create()
    post_meta.tables['tags_posts'].create()
    post_meta.tables['types'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['categories'].drop()
    post_meta.tables['categories_posts'].drop()
    post_meta.tables['posts'].drop()
    post_meta.tables['tags'].drop()
    post_meta.tables['tags_posts'].drop()
    post_meta.tables['types'].drop()
    post_meta.tables['users'].drop()
