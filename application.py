# Import functions and objects the microservice needs.
# - Flask is the top-level application. You implement the application by adding methods to it.
# - Response enables creating well-formed HTTP/REST responses.
# - requests enables accessing the elements of an incoming HTTP/REST request.
#
import json

# Setup and use the simple, common Python logging framework. Send log messages to the console.
# The application should get the log level out of the context. We will change later.
#

import os
import sys
import platform
import socket

import logging
from datetime import datetime

from flask import Flask, Response
from flask import request

from comment_service.service import CommentService

__comment_service = CommentService()


cwd = os.getcwd()
sys.path.append(cwd)
print("*** PYHTHONPATH = " + str(sys.path) + "***")


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Create the application server main class instance and call it 'application'
# Specific the path that identifies the static content and where it is.
application = Flask(__name__)


#
# NOTE NOTE NOTE
# Some of the following functions would be helper functions used in the organization.
# This means that they would be packages on a private or team package server.
# I do not want to set up a package server.
#

# 1. Extract the input information from the requests object.
# 2. Log the information
# 3. Return extracted information.
#

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        else:
            return json.JSONEncoder.default(self, obj)

def log_and_extract_input(method, path_params=None):
    path = request.path
    args = dict(request.args)
    data = None
    headers = dict(request.headers)
    method = request.method

    try:
        if request.data is not None:
            data = request.json
        else:
            data = None
    except Exception as e:
        # This would fail the request in a more real solution.
        data = "You sent something but I could not get JSON out of it."

    log_message = str(datetime.now()) + ": Method " + method

    inputs =  {
        "path": path,
        "method": method,
        "path_params": path_params,
        "query_params": args,
        "headers": headers,
        "body": data
        }

    log_message += " received: \n" + json.dumps(inputs, indent=2)
    logger.debug(log_message)

    return inputs


def log_response(method, status, data, txt):

    msg = {
        "method": method,
        "status": status,
        "txt": txt,
        "data": data
    }

    logger.debug(str(datetime.now()) + ": \n" + json.dumps(msg, indent=2, default=str))


# This function performs a basic health check. We will flesh this out.
@application.route("/api/health", methods=["GET"])
def health_check():

    pf = platform.system()

    rsp_data = { "status": "healthy", "time": str(datetime.now()),
                 "platform": pf,
                 "release": platform.release()
                 }

    if pf == "Darwin":
        rsp_data["note"]= "For some reason, macOS is called 'Darwin'"


    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    rsp_data["hostname"] = hostname
    rsp_data["IPAddr"] = IPAddr

    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


logger.debug("__name__ = " + str(__name__))

@application.route("/api/comments/comment", methods=["GET", "DELETE", "POST"])
def comments():
    req_info = log_and_extract_input("/api/comments/comment")

    try:
        if req_info["method"] == "POST":
            data = req_info["body"]
            res = __comment_service.add_comment(data["cid"], data["uid"], data["comment"])

            if res is not None:
                print(res["Attributes"])
                rsp = Response(json.dumps(res), status=200, content_type="text/plain")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")
    except Exception as e:
        """
        Non-specific, broad except clauses are a bad practice/design.
        """
        rsp = Response("I'm a teapot", status=418, content_type="text/plain")
        logger.error("comment: Exception=" + e)

    log_response("/api/comments/comment", rsp.status, rsp.data, "")
    return rsp

@application.route("/api/comments/content", methods=["DELETE", "POST"])
def content():
    req_info = log_and_extract_input("/api/comments/content")

    try:
        if req_info["method"] == "POST":
            data = req_info["body"]
            res = __comment_service.add_content(data["uid"], data["content"])
            if res is not None:
                rsp = Response(json.dumps(res), status=200, content_type="text/plain")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")
    except Exception as e:
        """
        Non-specific, broad except clauses are a bad practice/design.
        """
        rsp = Response("I'm a teapot", status=418, content_type="text/plain")
        logger.error("comment: Exception=" + e)

    log_response("/api/comments/comment", rsp.status, rsp.data, "")
    return rsp

@application.route("/api/comment/<id>", methods=["GET"])
def comment(id):
    req_info = log_and_extract_input("/api/comment", id)
    print("wrgwergwerhgewrh", id)

    try:
        if req_info["method"] == "GET":
            res = __comment_service.get_by_comment_id(id)

            if res is not None:
                rsp = Response(json.dumps(res), status=200, content_type="application/json")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")
    except Exception as e:
        """
        Non-specific, broad except clauses are a bad practice/design.
        """
        rsp = Response("I'm a teapot", status=418, content_type="text/plain")
        logger.error("comment: Exception=" + e)

    log_response("/api/comments/<id>", rsp.status, rsp.data, "")
    return rsp
@application.route("/succes")
def index():
    rsp = Response("welcome", status=200, content_type="text/plain")
    return rsp
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.run("0.0.0.0", port=5000)
    #application.run("10.1.188.234", port=5001)