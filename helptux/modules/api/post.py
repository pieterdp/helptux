from datetime import datetime
import pytz
from helptux.modules.api.generic import GenericApi
from helptux.models.post import Post
from helptux import db
from helptux.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist
import helptux.modules.api.type
import helptux.modules.api.user
import helptux.modules.api.category
import helptux.modules.api.tag


class PostApi(GenericApi):
    complex_params = ['categories', 'tags']
    simple_params = ['title', 'content', 'creation_time', 'last_modified', 'is_visible', 'is_deleted', 'type_id',
                     'author_id']
    required_params = ['title', 'type_id', 'author_id']
    no_update_params = ['last_modified', 'creation_time']
    possible_params = simple_params + complex_params

    def __init__(self):
        self.a_type = helptux.modules.api.type.TypeApi()
        self.a_user = helptux.modules.api.user.UserApi()

    def create(self, input_data, author_id=None):
        """
        Create a new post. See TagApi.create(). It is created by the user referred to by author_id and is of the
        type type_id.
        :param input_data:
        :param author_id:
        :return:
        """
        if not author_id:
            raise RequiredAttributeMissing('No author provided.')
        try:
            author = self.a_user.read(author_id)
        except DatabaseItemDoesNotExist:
            raise Exception('Author {0} does not exist.'.format(author_id))
        else:
            input_data['author_id'] = author_id
        cleaned_data = self.clean_input(input_data)
        try:
            existing_post = self.get_by_title(cleaned_data['title'])
        except DatabaseItemDoesNotExist:
            existing_post = None
        if existing_post:
            raise DatabaseItemAlreadyExists('A post with title {0} already exists'.format(cleaned_data['title']))

        new_post = Post(title=cleaned_data['title'], content=cleaned_data['content'],
                        creation_time=cleaned_data['creation_time'], last_modified=cleaned_data['last_modified'],
                        is_visible=cleaned_data['is_visible'], is_deleted=cleaned_data['is_deleted'])
        db.session.add(new_post)
        db.session.commit()
        type_id = cleaned_data['type_id']
        author_id = cleaned_data['author_id']
        # Add the type
        o_type = self.a_type.read(type_id)
        new_post.type = o_type
        # Add the author
        o_author = self.a_user.read(author_id)
        new_post.author = o_author
        # Add the tags
        for tag in cleaned_data['tags']:
            new_post.tags.append(self.new_tag(tag))
        # Add the categories
        for cat in cleaned_data['categories']:
            new_post.categories.append(self.new_category(cat))
        # Commit
        db.session.commit()
        return new_post

    def read(self, post_id):
        """
        Get a post by ID
        :param post_id:
        :return:
        """
        existing_post = Post.query.filter(Post.id == post_id).first()
        if existing_post is None:
            raise DatabaseItemDoesNotExist('No post with id {0}'.format(post_id))
        return existing_post

    def list(self):
        """
        Return all posts
        :return:
        """
        existing_posts = Post.query.all()
        return existing_posts

    def update(self, post_id, input_data, author_id=None):
        """
        Update an existing post. See self.create() and TagApi.update().
        :param post_id:
        :param input_data:
        :param author_id:
        :return:
        """
        if not author_id:
            raise RequiredAttributeMissing('No author provided.')
        try:
            author = self.a_user.read(author_id)
        except DatabaseItemDoesNotExist:
            raise Exception('Author {0} does not exist.'.format(author_id))
        else:
            input_data['author_id'] = author_id
        cleaned_data = self.clean_input(input_data)
        existing_post = self.read(post_id)
        for no_update_param in self.no_update_params:
            cleaned_data[no_update_param] = getattr(existing_post, no_update_param)
        cleaned_data['last_modified'] = datetime.now(tz=pytz.timezone('Europe/Brussels'))
        type_id = cleaned_data['type_id']
        author_id = cleaned_data['author_id']
        # Update simple attributes
        existing_post = self.update_simple_attributes(existing_post, self.simple_params, cleaned_data)
        # Add the type
        o_type = self.a_type.read(type_id)
        existing_post.type = o_type
        # Add the author
        o_author = self.a_user.read(author_id)
        existing_post.author = o_author
        # Remove all tags
        existing_post = self.remove_tags(existing_post)
        for tag in cleaned_data['tags']:
            existing_post.tags.append(self.new_tag(tag))
        # Remove all categories
        existing_post = self.remove_categories(existing_post)
        for cat in cleaned_data['categories']:
            existing_post.categories.append(self.new_category(cat))
        # Commit
        db.session.commit()
        return existing_post

    def delete(self, post_id):
        """
        Delete an existing post. See TagApi.delete()
        :param post_id:
        :return:
        """
        existing_post = self.read(post_id)
        db.session.delete(existing_post)
        db.session.commit()
        return True

    def get_by_title(self, post_title):
        existing_post = Post.query.filter(Post.title == post_title).first()
        if existing_post is None:
            raise DatabaseItemDoesNotExist('No post with title {0}'.format(post_title))
        return existing_post

    def new_tag(self, tag_data):
        a_tag = helptux.modules.api.tag.TagApi()
        if 'tag' not in tag_data:
            raise RequiredAttributeMissing('Attribute tag missing for new tag')
        try:
            existing_tag = a_tag.get_by_tag(tag_data['tag'])
        except DatabaseItemDoesNotExist:
            existing_tag = a_tag.create(tag_data)
        return existing_tag

    def new_category(self, category_data):
        a_cat = helptux.modules.api.category.CategoryApi()
        if 'category' not in category_data:
            raise RequiredAttributeMissing('Attribute category missing for new category')
        try:
            existing_category = a_cat.get_by_category(category_data['category'])
        except DatabaseItemDoesNotExist:
            existing_category = a_cat.create(category_data)
        return existing_category

    def remove_categories(self, entity):
        for cat in entity.categories:
            entity.categories.remove(cat)
        db.session.commit()
        return entity

    def remove_tags(self, entity):
        for tag in entity.tags:
            entity.tags.remove(tag)
        db.session.commit()
        return entity

    def convert_date_from_string_to_datetime(self, date_string):
        if type(date_string) is str:
            return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
        else:
            return str

    def clean_input(self, unclean_data):
        # TODO: clean html tags (everywhere)
        cleaned_data = self.clean_input_data(unclean_data, complex_params=self.complex_params,
                                             possible_params=self.possible_params, required_params=self.required_params)
        if cleaned_data['last_modified']:
            cleaned_data['last_modified'] = self.convert_date_from_string_to_datetime(cleaned_data['last_modified'])
        else:
            cleaned_data['last_modified'] = datetime.now(tz=pytz.timezone('Europe/Brussels'))
        if cleaned_data['creation_time']:
            cleaned_data['creation_time'] = self.convert_date_from_string_to_datetime(cleaned_data['creation_time'])
        else:
            cleaned_data['creation_time'] = datetime.now(tz=pytz.timezone('Europe/Brussels'))
        if not cleaned_data['is_visible']:
            cleaned_data['is_visible'] = True
        if not cleaned_data['is_deleted']:
            cleaned_data['is_deleted'] = False
        return cleaned_data
