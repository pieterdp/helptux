from helptux.modules.api.generic import GenericApi
from helptux.models.user import Role
from helptux import db, login_manager
from helptux.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist,\
    InvalidPassword


class RoleApi(GenericApi):
    complex_params = []
    simple_params = ['role']
    required_params = ['role']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        """
        Add a new role. See TagApi.create().
        :param input_data:
        :return:
        """
        cleaned_data = self.clean_input(input_data)
        try:
            existing_role = self.get_by_role(cleaned_data['role'])
        except DatabaseItemDoesNotExist:
            existing_role = None
        if existing_role:
            raise DatabaseItemAlreadyExists('A role called {0} already exists.'.format(input_data['email']))
        new_role = Role(role=cleaned_data['role'])
        db.session.add(new_role)
        db.session.commit()
        return new_role

    def read(self, role_id):
        """
        Get a role by its id
        :param role_id:
        :return:
        """
        existing_role = Role.query.filter(Role.id == role_id).first()
        if existing_role is None:
            raise DatabaseItemDoesNotExist('No role with id {0}'.format(role_id))
        return existing_role

    def update(self, role_id, input_data):
        """
        Update a role
        :param role_id:
        :param input_data:
        :return:
        """
        cleaned_data = self.clean_input(input_data)
        existing_role = self.read(role_id)
        # Update existing roles
        existing_role = self.update_simple_attributes(existing_role, self.simple_params, cleaned_data)
        db.session.commit()
        return existing_role

    def delete(self, role_id):
        """
        Delete a role
        :param role_id:
        :return:
        """
        existing_role = self.read(role_id)
        db.session.remove(existing_role)
        db.session.commit()
        return True

    def list(self):
        """
        List all roles
        :return:
        """
        existing_roles = Role.query.all()
        return existing_roles

    def clean_input(self, unclean_data):
        cleaned_data = self.clean_input_data(unclean_data, complex_params=self.complex_params,
                                             possible_params=self.possible_params, required_params=self.required_params)
        return cleaned_data

    def get_by_role(self, input_role):
        existing_role = Role.query.filter_by(Role.role == input_role).first()
        if existing_role is None:
            raise DatabaseItemDoesNotExist('No role called {0}'.format(input_role))
        return existing_role
