import boto3
import re
import json
from botocore.exceptions import ClientError

import iris_settings
from iris_data.exceptions import IrisStorageError


class IrisSessionData:

    def __init__(self):

        self.client = boto3.client('s3')
        self.replacement_pattern = None

    def store_data(self, session_id, data):
        """
        store data for session
        :param session_id: id for the session, should be uuid4
        :param data: data to store
        """
        try:
            self.client.put_object(Bucket=iris_settings.IRIS_SESSION_BUCKET, Key="session/" + session_id, Body=data)
        except ClientError:
            raise IrisStorageError("Error storing data")

    def store_json_data(self, session_id, json_data):
        """
        store a python object that can serialize to json for the given session
        :param session_id: id for the session, should be uuid4
        :param json_data: a python object that can serialize to json
        """
        self.store_data(session_id, json.dumps(json_data))

    def get_data(self, session_id):
        """
        get data for session
        :param session_id: id for the session, should be uuid4
        :return: byte[] of store data
        """
        try:
            response = self.client.get_object(Bucket=iris_settings.IRIS_SESSION_BUCKET, Key="session/" + session_id)
            return response['Body'].read()
        except ClientError:
            raise IrisStorageError("Error getting data")

    def get_json_data(self, session_id):
        """
        get json data for session
        :param session_id: id for the session, should be uuid4
        :return: python object from deserialized json
        """
        return json.loads(self.get_data(session_id))

    def store_shared_json_data(self, shared_id, json_data):

        """
        store a shared json blob under the given id which can be referenced from store json documents
        :param shared_id: id for the shared data, should be uuid4
        :param json_data: a python object that can serialize to json
        """
        try:
            self.client.put_object(Bucket=iris_settings.IRIS_SESSION_BUCKET, Key="shared/" + shared_id,
                                   Body=json.dumps(json_data))
        except ClientError:
            raise IrisStorageError("Error storing data")

    def get_shared_json_data(self, shared_id):
        """
        retrieve a shared json blov for the given id
        :param shared_id:  id for the shared data, should be uuid4
        :return:  python object from deserialized json
        """
        try:
            response = self.client.get_object(Bucket=iris_settings.IRIS_SESSION_BUCKET, Key="shared/" + shared_id)
            return json.loads(response['Body'].read())
        except ClientError:
            raise IrisStorageError("Error getting data")

    def expand_json_obj(self, obj):

        """
        expand the given object by looking for strings like [[<type>:<id>]] and replace with common or shared json
        :param obj: python object from deserialized json
        :return: expanded python object
        """
        common = obj.get("common", [])
        return self.traverse_replace(obj, common)

    def traverse_replace(self, obj, common, shared=None):

        if shared is None:
            shared = {}

        if self.replacement_pattern is None:
            self.replacement_pattern = re.compile("\[\[(.*?):(.*?)\]\]")
        if isinstance(obj, dict):
            return {k: self.traverse_replace(v, common) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.traverse_replace(elem, common) for elem in obj]
        else:
            if isinstance(obj, str):
                match = self.replacement_pattern.match(obj)
                if match:
                    replacement_type = match.group(1)
                    replacement_id = match.group(2)
                    if replacement_type == "common":
                        replacement = common.get(replacement_id)
                        if replacement:
                            return replacement
                    elif replacement_type == "shared":
                        if replacement_id not in shared:
                            shared[replacement_id] = self.get_shared_json_data(replacement_id)
                        return shared[replacement_id]
            return obj
