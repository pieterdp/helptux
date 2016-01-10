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
        pass

    def read(self, role_id):
        pass

    def update(self, role_id, input_data):
        pass

    def delete(self, role_id):
        pass
