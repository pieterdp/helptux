from flask import make_response
import json
from helptux.modules.api.post import PostApi
from helptux.modules.api.category import CategoryApi
from helptux.modules.api.tag import TagApi
from helptux.modules.api.type import TypeApi
from helptux.modules.error import DatabaseItemDoesNotExist, DatabaseItemAlreadyExists, RequiredAttributeMissing
from helptux.modules.msg.messages import api_msg, error_msg
from helptux import app


class HelptuxApi:
    def __init__(self, api_class):
        self.api = api_class()
        self.msg = None

    def create(self, input_data, additional_opts):
        try:
            created_object = self.api.create(input_data=input_data, **additional_opts)
        except DatabaseItemAlreadyExists:
            self.msg = error_msg['item_exists'].format(self.api)
            created_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            created_object = None
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
            found_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            found_object = None
        else:
            self.msg = api_msg['item_read'].format(self.api, item_id)
        if found_object is not None:
            return found_object.output_obj()
        else:
            return u''

    def update(self, item_id, input_data, additional_opts):
        try:
            updated_object = self.api.update(item_id, input_data=input_data, **additional_opts)
        except DatabaseItemDoesNotExist:
            self.msg = error_msg['item_not_exists'].format(self.api, item_id)
            updated_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            updated_object = None
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
            deleted_object = None
        except Exception as e:
            self.msg = error_msg['error_occurred'].format(e)
            deleted_object = None
        else:
            self.msg = api_msg['item_deleted'].format(self.api, item_id)
        if deleted_object is True:
            return u''
        else:
            return u''

    def response(self, data):
        """
        Create an API response
        :param data:
        :param msg:
        :return:
        """
        resp = make_response()
        resp.headers['Content-Type'] = 'application/json'
        resp.data = json.dumps({
            'msg': self.msg,
            'data': data
        })
        return resp

