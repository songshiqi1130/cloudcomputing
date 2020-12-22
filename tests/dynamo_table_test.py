
from DataAccessLayer.DynamoDBDataTable import DynamoDBDataTable as DynamoDBTable
import  json


def t1():
    connect_info = {"aws_access_key_id": "AKIA3YJ5IVZZ37FYER5E",
                    "aws_secret_access_key": "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",
                    "region_name": "us-east-1"}
    key = "comment_id"
    t1 = DynamoDBTable("comment", connect_info, key)
    print("t1 = ", t1)

def t2():
    connect_info = {"aws_access_key_id": "AKIA3YJ5IVZZ37FYER5E",
                    "aws_secret_access_key": "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",
                    "region_name": "us-east-1"}
    t1 = DynamoDBTable("comments", connect_info, "comment_id")
    res = t1.find_by_primary_key(key_fields="1001")

    print("ts -- res = ", json.dumps(res, indent=3))

def t3():
    connect_info = {"aws_access_key_id": "AKIA3YJ5IVZZ37FYER5E",
                    "aws_secret_access_key": "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",
                    "region_name": "us-east-1"}
    t1 = DynamoDBTable("comments", connect_info, "comment_id")
    response_email = "ss58851@columbia.edu"
    response = "To cool for school"
    res = t1.add_respone("1001", response_email, response)
    print("t2 -- res = ", json.dumps(res, indent=3))
def t4():
    connect_info = {"aws_access_key_id": "AKIA3YJ5IVZZ37FYER5E",
                    "aws_secret_access_key": "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",
                    "region_name": "us-east-1"}
    t1 = DynamoDBTable("comments", connect_info, "comment_id")
    response_email = "ss5885333@columbia.edu"
    res = t1.add_content(response_email)
    print("t2 -- res = ", json.dumps(res, indent=3))
# t1()
t2()
# t3()