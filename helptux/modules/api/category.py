from helptux.modules.api.generic import GenericApi
from helptux.models.post import Category
from helptux import db
from helptux.modules.error import RequiredAttributeMissing, DatabaseItemAlreadyExists, DatabaseItemDoesNotExist


class CategoryApi(GenericApi):
    complex_params = []
    simple_params = ['category']
    required_params = ['category']
    possible_params = simple_params + complex_params

    def create(self, input_data):
        """
        Create a new category. See TagApi.create()
        :param input_data:
        :return:
        """
        cleaned_data = self.clean_input_data(input_data, complex_params=self.complex_params,
                                             possible_params=self.possible_params, required_params=self.required_params)
        try:
            existing_category = self.get_by_category(cleaned_data['category'])
        except DatabaseItemDoesNotExist:
            existing_category = None
        if existing_category:
            raise DatabaseItemAlreadyExists('A category called {0} already exists'.format(existing_category.category))

        new_category = Category(category=cleaned_data['category'])
        db.session.add(new_category)
        db.session.commit()
        return new_category

    def read(self, category_id):
        """
        Given a category_id, return the corresponding Category database entity. Fails if one doesn't exist.
        :param category_id:
        :return:
        """
        existing_category = Category.query.filter(Category.id == category_id).first()
        if existing_category is None:
            raise DatabaseItemDoesNotExist('No category with id {0}'.format(category_id))
        return existing_category

    def list(self):
        """
        Return all categories
        :return:
        """
        existing_categories = Category.query.all()
        return existing_categories

    def update(self, category_id, input_data):
        """
        Update a category identified by rag_id. The variable input_data must contain all variables, both
        those that are to be changed and those that remain the same. If you only send the changed ones, the others
        will be set to None. It follows the same logic as self.create(), but it doesn't die when the category already
        exists (but it does when it doesn't).
        :param category_id:
        :param input_data:
        :return:
        """
        existing_category = self.read(category_id)
        cleaned_data = self.clean_input_data(input_data, complex_params=self.complex_params,
                                             possible_params=self.possible_params, required_params=self.required_params)
        existing_category = self.update_simple_attributes(existing_category, self.simple_params, cleaned_data)
        db.session.commit()
        return existing_category

    def delete(self, category_id):
        """
        Delete a category identified by category_id. Fails if one doesn't exist.
        :param category_id:
        :return:
        """
        existing_category = self.read(category_id)
        db.session.delete(existing_category)
        db.session.commit()
        return True

    def get_by_category(self, category_name):
        """
        Get a category object by its .category attribute (exact match)
        :param category_name:
        :return:
        """
        existing_category = Category.query.filter(Category.category == category_name).first()
        if existing_category is None:
            raise DatabaseItemDoesNotExist('No category called {0}'.format(category_name))
        else:
            return existing_category
