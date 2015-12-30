from helptux.modules.api.generic import GenericApi
from helptux.models.post import User
from helptux import db
from helptux.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist


class UserApi(GenericApi):
    complex_params = []
    simple_params = []
    required_params = []
    possible_params = simple_params + complex_params

    def create(self, input_data):
        """
        Add a new user. See TagApi.create().
        :param input_data:
        :return:
        """
        pass

    def read(self, user_id):
        """
        Return a user by its id.
        :param user_id:
        :return:
        """
        existing_user = User.query.filter(User.id == user_id).first()
        if existing_user is None:
            raise DatabaseItemDoesNotExist('No user with id {0}'.format(user_id))
        return existing_user

    def update(self, user_id, input_data):
        pass

    def delete(self, user_id):
        """
        Delete a user identified by user_id. See TagApi.delete()
        :param user_id:
        :return:
        """
        existing_user = self.read(user_id)
        db.session.delete(existing_user)
        db.session.commit()
        return True

    def get_by_user(self, user_name):
        existing_user = User.query.filter(User.username == user_name).first()
        if existing_user is None:
            raise DatabaseItemDoesNotExist('No user called {0}'.format(user_name))
        return existing_user
