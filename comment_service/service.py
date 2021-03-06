
#
# The service would use a factory or configuration to determine which implementation
# of BaseDataTable to get. I am not going to bother to do that and import the table
# for the backend that the service uses.
#
# https://en.wikipedia.org/wiki/Factory_method_pattern
#
from DataAccessLayer.DynamoDBDataTable import DynamoDBDataTable

class CommentService:
    """
    In some designs, this class would inherit from a base framework class for implementing services.

    Example of some REST/web application frameworks are at
    https://hub.packtpub.com/which-python-framework-is-best-for-building-restful-apis-django-or-flask/

    There are many, many frameworks for all languages and application servers.
    """

    # Again, this would not be hardcoded and would come from the configuration/environment.
    __table_name = "comments"

    def __init__(self):
        self._table_name = CommentService.__table_name
        self._data_table = DynamoDBDataTable(self._table_name, key_columns="comment_id")

    def get_by_uid(self, uid):
        result = self._data_table.find_by_uid(uid)
        return result

    def add_comment(self, cid, uid, comment_text):
        result = self._data_table.add_comment(cid, uid, comment_text, email=None)
        return result

    def add_content(self, uid, comment_text):
        result = self._data_table.add_content(uid, comment_text, email=None)
        return result

    def get_by_date_time(self):
        result = self._data_table.find_by_date_time()
        return result

