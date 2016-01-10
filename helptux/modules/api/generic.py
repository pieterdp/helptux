from helptux.modules.error import RequiredAttributeMissing, DatabaseItemDoesNotExist


class GenericApi:

    def clean_input_data(self, input_data, possible_params, required_params, complex_params):
        """
        Clean the input data dict: remove all non-supported attributes and check whether all the required
        parametes have been filled. All missing parameters are set to None. All attributes in complex_params
        must be a list.
        :param input_data:
        :param required_params
        :param possible_params
        :param complex_params
        :return:
        """
        cleaned = {}
        # All non-supported parameters are filtered
        for input_data_key, input_data_value in input_data.items():
            if input_data_key in possible_params:
                cleaned[input_data_key] = input_data_value
        # Check whether the required parameters are used
        for required_param in required_params:
            if required_param not in input_data:
                raise RequiredAttributeMissing('Missing {0} in input_data'.format(required_param))
        # Set the missing attributes from possible_params in input_data to None
        for possible_param in possible_params:
            if possible_param not in cleaned:
                cleaned[possible_param] = None
        # Check whether the complex parameters are lists
        for complex_param in complex_params:
            if type(cleaned[complex_param]) is not list:
                cleaned[complex_param] = [cleaned[complex_param]]
        return cleaned

    def update_entity_attribute(self, entity, attribute_name, attribute_new_value):
        """
        This function updates the attribute attribute_name of entity only if the original value
        is different from attribute_new_value
        :param entity:
        :param attribute_name:
        :param attribute_value:
        :return:
        """
        original_value = getattr(entity, attribute_name)
        if original_value != attribute_new_value:
            setattr(entity, attribute_name, attribute_new_value)
        return entity

    def update_simple_attributes(self, entity, simple_attributes, cleaned_data):
        """
        Use self.update_entity_attribute() to update the simple (string or numeric) attributes of entity with
        cleaned_data.
        :param entity:
        :param simple_attributes:
        :param cleaned_data:
        :return:
        """
        for simple_attribute in simple_attributes:
            entity = self.update_entity_attribute(entity, simple_attribute, cleaned_data[simple_attribute])
        return entity
