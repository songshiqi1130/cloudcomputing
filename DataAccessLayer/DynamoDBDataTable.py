
from DataAccessLayer.BaseDataTable import BaseDataTable, DataTableException
import utilities.context as ctx
import uuid
import time

import boto3
from boto3.dynamodb.conditions import Key, Attr
import json


class DynamoDBDataTable(BaseDataTable):

    def __init__(self, table_name, connect_info=None, key_columns=None, context=None):

        self._table_name = table_name
        self._key_columns = key_columns

        if connect_info is not None:
            self._connect_info = connect_info
        else:
            self._connect_info = {"aws_access_key_id": "AKIA3YJ5IVZZ37FYER5E",
                        "aws_secret_access_key": "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",
                        "region_name": "us-east-1"}

        self._dynamodb = boto3.resource('dynamodb',
                                  aws_access_key_id=self._connect_info["aws_access_key_id"],
                                  aws_secret_access_key=self._connect_info["aws_secret_access_key"],
                                  region_name=self._connect_info["region_name"])



        #self._other_client = boto3.client("dynamodb")

        self._dynamo_table = self._dynamodb.Table(table_name)

    def find_by_primary_key(self):
        return

    def find_by_uid(self, uid):
        """
        :param key_fields: The values for the key_columns, in order, to use to find a record. For example,
            for Appearances this could be ['willite01', 'BOS', '1960']
        :param field_list: A subset of the fields of the record to return. The CSV file or RDB table may have many
            additional columns, but the caller only requests this subset.
        :return: None, or a dictionary containing the columns/values for the row.
        """
        response = self._dynamo_table.scan(
            FilterExpression=Attr('uid').eq(uid)
        )
        return response['Items']

    def find_by_date_time(self):
        """
        :param key_fields: The values for the key_columns, in order, to use to find a record. For example,
            for Appearances this could be ['willite01', 'BOS', '1960']
        :param field_list: A subset of the fields of the record to return. The CSV file or RDB table may have many
            additional columns, but the caller only requests this subset.
        :return: None, or a dictionary containing the columns/values for the row.
        """
        dt = time.time()
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt)),
        response = self._dynamo_table.scan(
            FilterExpression=Attr('date_time').begins_with('2')
        )
        return response['Items']

    def find_by_template(self, template, field_list=None, limit=None, offset=None, order_by=None, context=None):
        """

        :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}. The function will return
            a derived table containing the rows that match the template.
        :param field_list: A list of requested fields of the form, ['fielda', 'fieldb', ...]
        :param limit: Do not worry about this for now.
        :param offset: Do not worry about this for now.
        :param order_by: Do not worry about this for now.
        :return: A derived table containing the computed rows.
        """
        pass

    def insert(self, new_entity, context=None):
        """

        :param new_record: A dictionary representing a row to add to the set of records. Raises an exception if this
            creates a duplicate primary key.
        :return: None
        """

        # dt = time.time()
        # dts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt))
        #
        # item = {
        #     "comment_id": str(uuid.uuid4()),
        #     "version_id": str(uuid.uuid4()),
        #     "email": email,
        #     "comment": comment,
        #     "tags": tags,
        #     "datetime": dts,
        #     "responses": []
        # }
        #
        # res = self._dynamo_table.("comment", item=new_entity)
        #
        # return res
        pass

    def delete_by_template(self, template, context=None):
        """

        Deletes all records that match the template.

        :param template: A template.
        :return: A count of the rows deleted.
        """
        pass

    def delete_by_key(self, key_fields, Context=None):
        """

        Delete record with corresponding key.

        :param key_fields: List containing the values for the key columns
        :return: A count of the rows deleted.
        """
        pass

    def update_by_template(self, template, new_values, context=None):
        """

        :param template: A template that defines which matching rows to update.
        :param new_values: A dictionary containing fields and the values to set for the corresponding fields
            in the records. This returns an error if the update would create a duplicate primary key. NO ROWS are
            update on this error.
        :return: The number of rows updates.
        """
        pass

    def update_by_key(self, key_fields, new_values, context=None):
        """

        :param key_fields: List of values for primary key fields
        :param new_values: A dictionary containing fields and the values to set for the corresponding fields
            in the records. This returns an error if the update would create a duplicate primary key. NO ROWS are
            update on this error.
        :return: The number of rows updates.
        """
        pass

    def query(self, query_statement, args, context=None):
        """
        Passed through/executes a raw query in the native implementation language of the backend.
        :param query_statement: Query statement as a string.
        :param args: Args to insert into query if it is a template
        :param context:
        :return: A JSON object containing the result of the operation.
        """
        pass

    def load(self, rows=None):
        """
        Loads data into the data table.
        :param rows:
        :return: Number of rows loaded.
        """

    def save(self, context):
        """
        Writes any cached data to a backing store.
        :param context:
        :return:
        """
    def add_comment(self, key_fields, response_uid, response_text, email):
        kf = {
            self._key_columns : key_fields
        }
        if not email:
            response_email = ""
        dt = time.time()
        full_rsp = {
            "email": response_email,
            "date_time": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt)),
            "response_text": response_text,
            "response_id": str(uuid.uuid4()),
            "uid":response_uid
        }
        UpdateExpression = "SET responses = list_append(responses, :i)"
        ExpressionAttributeValues = {
            ':i': [full_rsp]
        }
        ReturnValues = "UPDATED_NEW"
        res = self._dynamo_table.update_item(
            Key=kf,
            UpdateExpression=UpdateExpression,
            ExpressionAttributeValues=ExpressionAttributeValues,
            ReturnValues=ReturnValues
        )
        return res

    def add_content(self, uid, content, email):
        dt = time.time()
        if not email:
            email = ""
        item = {
            "email": email,
            "date_time": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt)),
            "uid": uid,
            "comment_id": str(uuid.uuid4()),
            "comment_text": content
        }
        res = self._dynamo_table.put_item(
            Item=item
        )
        return res

