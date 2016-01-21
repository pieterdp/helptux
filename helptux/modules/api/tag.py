from helptux.modules.api.generic import GenericApi
from helptux.models.post import Tag
from helptux import db
from helptux.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist


class TagApi(GenericApi):
    complex_params = []
    simple_params = ['tag']
    required_params = ['tag']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        """
        Create a new tag. The data input variable contains all the attributes for the "tag" entity
        in the database as a dict. For simple attributes, this is a string or integer value, but for complex attributes
        (relationships), it is a dictionary containing the attributes for the respective entity
        in the database.
        The function will fail when a tage with the same "tag" attribute already exists in the same
        section.
        The function returns the tag sqlalchemy object.
        :param input_data:
        :return:
        """
        cleaned_data = self.clean_input_data(input_data, complex_params=self.complex_params,
                                             possible_params=self.possible_params, required_params=self.required_params)
        try:
            existing_tag = self.get_by_tag(cleaned_data['tag'])
        except DatabaseItemDoesNotExist:
            existing_tag = None
        if existing_tag:
            raise DatabaseItemAlreadyExists('A tag called {0} already exists'.format(existing_tag.tag))

        new_tag = Tag(tag=cleaned_data['tag'])
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

    def read(self, tag_id):
        """
        Given a tag_id, return the corresponding Tag database entity. Fails if one doesn't exist.
        :param tag_id:
        :return:
        """
        existing_tag = Tag.query.filter(Tag.id == tag_id).first()
        if existing_tag is None:
            raise DatabaseItemDoesNotExist('No tag with id {0}'.format(tag_id))
        return existing_tag

    def list(self):
        """
        Return all tags
        :return:
        """
        existing_tags = Tag.query.all()
        return existing_tags

    def update(self, tag_id, input_data):
        """
        Update a tag identified by rag_id. The variable input_data must contain all variables, both
        those that are to be changed and those that remain the same. If you only send the changed ones, the others
        will be set to None. It follows the same logic as self.create(), but it doesn't die when the tag already
        exists (but it does when it doesn't).
        :param tag_id:
        :param input_data:
        :return:
        """
        existing_tag = self.read(tag_id)
        cleaned_data = self.clean_input_data(input_data, complex_params=self.complex_params,
                                             possible_params=self.possible_params, required_params=self.required_params)
        existing_tag = self.update_simple_attributes(existing_tag, self.simple_params, cleaned_data)
        db.session.commit()
        return existing_tag

    def delete(self, tag_id):
        """
        Delete a tag identified by tag_id. Fails if one doesn't exist.
        :param tag_id:
        :return:
        """
        existing_tag = self.read(tag_id)
        db.session.delete(existing_tag)
        db.session.commit()
        return True

    def get_by_tag(self, tag_name):
        """
        Get a tag object by its .tag attribute (exact match)
        :param tag:
        :return:
        """
        existing_tag = Tag.query.filter(Tag.tag == tag_name).first()
        if existing_tag is None:
            raise DatabaseItemDoesNotExist('No tag called {0}'.format(tag_name))
        else:
            return existing_tag
