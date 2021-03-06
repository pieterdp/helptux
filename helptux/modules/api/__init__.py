from flask import make_response
import json
from helptux.modules.api.post import PostApi
from helptux.modules.api.tag import TagApi
from helptux.modules.api.type import TypeApi
from helptux.modules.error import DatabaseItemDoesNotExist, DatabaseItemAlreadyExists, RequiredAttributeMissing
from helptux.modules.msg.messages import api_msg, error_msg
from helptux import app


class HelptuxApi:
    def __init__(self, api_class, o_request, api_obj_id=None, additional_opts=None):
        self.api = api_class()
        self.request = o_request
        self.msg = None
        self.output_data = u''
        if not additional_opts:
            additional_opts = {}
        ##
        # Every request method has a self.action() defined:
        #   GET => self.read(api_obj_id)
        #   DELETE => self.delete(api_obj_id)
        #   PUT => self.update(api_obj_id)
        #   POST => self.create()
        ##
        input_data_raw = self.request.get_data()
        input_data_string = input_data_raw.decode('utf-8')
        self.response = make_response()
        if self.request.method == 'GET':
            if api_obj_id is None:
                if hasattr(self.api, 'list'):
                    self.output_data = self.list()
                else:
                    self.msg = error_msg['missing_argument'].format('api_obj_id')
                    self.response.status_code = 400
            else:
                self.output_data = self.read(api_obj_id)
        elif self.request.method == 'DELETE':
            if api_obj_id is None:
                self.msg = error_msg['missing_argument'].format('api_obj_id')
                self.response.status_code = 400
            else:
                self.output_data = self.delete(api_obj_id)
        elif self.request.method == 'PUT':
            if api_obj_id is None:
                self.msg = error_msg['missing_argument'].format('api_obj_id')
                self.response.status_code = 400
            else:
                if self.parse_json(input_data_string) is not None:
                    self.output_data = self.update(api_obj_id, self.parse_json(input_data_string), additional_opts)
        elif self.request.method == 'POST':
            if self.parse_json(input_data_string) is not None:
                self.output_data = self.create(self.parse_json(input_data_string), additional_opts)
        else:
            self.msg = error_msg['illegal_action'].format(self.request.method)
            self.response.status_code = 405
        ##
        # Set self.response
        ##
        self.headers()
        self.create_response(self.output_data)

    def create(self, input_data, additional_opts=None):
        if not additional_opts:
            additional_opts = {}
        try:
            created_object = self.api.create(input_data=input_data, **additional_opts)
        except DatabaseItemAlreadyExists:
            self.msg = error_msg['item_exists'].format(self.api)
            self.response.status_code = 400
            created_object = None
        #except Exception as e:
        #    self.msg = error_msg['error_occurred'].format(e)
        #    self.response.status_code = 400
        #    created_object = None
        else:
            self.msg = api_msg['item_created'].format(self.api, created_object.id)
        if created_object is not None:
            return created_object.output_obj()
        else:
            return u''

    def read(self, item_id):
        try:
            found_object = self.api.read(item_id)
        except DatabaseItemDoesNotExist:
            self.msg = error_msg['item_not_exists'].format(self.api, item_id)
            self.response.status_code = 404
            found_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            self.response.status_code = 400
            found_object = None
        else:
            self.msg = api_msg['item_read'].format(self.api, item_id)
        if found_object is not None:
            return found_object.output_obj()
        else:
            return u''

    def list(self):
        try:
            found_objects = self.api.list()
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            self.response.status_code = 400
            found_objects = None
        if found_objects is not None:
            output_objects = []
            for found_object in found_objects:
                output_objects.append(found_object.output_obj())
            return output_objects
        else:
            return u''

    def update(self, item_id, input_data, additional_opts=None):
        if not additional_opts:
            additional_opts = {}
        try:
            updated_object = self.api.update(item_id, input_data=input_data, **additional_opts)
        except DatabaseItemDoesNotExist:
            self.msg = error_msg['item_not_exists'].format(self.api, item_id)
            self.response.status_code = 404
            updated_object = None
        #except Exception as e:
        #    self.msg = error_msg['error_occurred'].format(e)
        #    self.response.status_code = 400
        #    updated_object = None
        else:
            self.msg = api_msg['item_updated'].format(self.api, updated_object.id)
        if updated_object is not None:
            return updated_object.output_obj()
        else:
            return u''

    def delete(self, item_id):
        try:
            deleted_object = self.api.delete(item_id)
        except DatabaseItemDoesNotExist:
            self.msg = error_msg['item_not_exists'].format(self.api, item_id)
            self.response.status_code = 404
            deleted_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            self.response.status_code = 400
            deleted_object = None
        else:
            self.msg = api_msg['item_deleted'].format(self.api, item_id)
        if deleted_object is True:
            return u''
        else:
            return u''

    def headers(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'

    def create_response(self, data):
        """
        Create an API response
        :param data:
        :return:
        """
        self.response.data = json.dumps({
            'msg': self.msg,
            'data': data
        })

    def parse_json(self, unparsed_string):
        try:
            parsed_string = json.loads(unparsed_string)
        except ValueError as e:
            self.msg = u'A JSON error occurred: {0}'.format(e)
            return None
        return parsed_string


