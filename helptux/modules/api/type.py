from helptux.modules.api.generic import GenericApi
from helptux.models.post import Type
from helptux import db
from helptux.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist


class TypeApi(GenericApi):
    complex_params = ['posts']
    simple_params = ['type']
    required_params = ['type']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        """
        Add a new type. See TagApi.create().
        :param input_data:
        :return:
        """
        cleaned_data = self.clean_input_data(input_data, possible_params=self.possible_params,
                                             complex_params=self.complex_params, required_params=self.required_params)
        try:
            existing_type = self.get_by_type(cleaned_data['type'])
        except DatabaseItemDoesNotExist:
            existing_type = None
        if existing_type:
            raise DatabaseItemAlreadyExists('A type called {0} already exists'.format(existing_type.type))

        new_type = Type(s_type=cleaned_data['type'])
        db.session.add(new_type)
        db.session.commit()
        return new_type

    def read(self, type_id):
        """
        Return a type by its id.
        :param type_id:
        :return:
        """
        existing_type = Type.query.filter(Type.id == type_id).first()
        if existing_type is None:
            raise DatabaseItemDoesNotExist('No type with id {0}'.format(type_id))
        return existing_type

    def list(self):
        """
        Return all types
        :return:
        """
        existing_types = Type.query.all()
        return existing_types

    def update(self, type_id, input_data):
        """
        Update a type identified by type_id with input_data. See TagApi.update() and TypeApi.create()
        :param type_id:
        :param input_data:
        :return:
        """
        cleaned_data = self.clean_input_data(input_data, possible_params=self.possible_params,
                                             complex_params=self.complex_params, required_params=self.required_params)
        existing_type = self.read(type_id)
        # Update simple attributes
        existing_type = self.update_simple_attributes(existing_type, self.simple_params, cleaned_data)
        db.session.commit()
        return existing_type

    def delete(self, type_id):
        """
        Delete a type identified by type_id. See TagApi.delete()
        :param type_id:
        :return:
        """
        existing_type = self.read(type_id)
        db.session.delete(existing_type)
        db.session.commit()
        return True

    def get_by_type(self, type_name):
        existing_type = Type.query.filter(Type.type == type_name).first()
        if existing_type is None:
            raise DatabaseItemDoesNotExist('No type called {0}'.format(type_name))
        return existing_type

    def remove_posts(self, entity):
        for post in entity.posts:
            entity.posts.remove(post)
        db.session.commit()
        return entity
