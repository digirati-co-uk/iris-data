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

        try:
            self.client.put_object(Bucket=iris_settings.IRIS_SESSION_BUCKET, Key="session/" + session_id, Body=data)
        except ClientError:
            raise IrisStorageError("Error storing data")

    def store_json_data(self, session_id, json_data):

        # TODO : comments for functions
        self.store_data(session_id, json.dumps(json_data))

    def get_data(self, session_id):

        try:
            response = self.client.get_object(Bucket=iris_settings.IRIS_SESSION_BUCKET, Key="session/" + session_id)
            return response['Body'].read()
        except ClientError:
            raise IrisStorageError("Error getting data")

    def get_json_data(self, session_id):

        return json.loads(self.get_data(session_id))

    def store_shared_json_data(self, shared_id, json_data):

        try:
            self.client.put_object(Bucket=iris_settings.IRIS_SESSION_BUCKET, Key="shared/" + shared_id,
                                   Body=json.dumps(json_data))
        except ClientError:
            raise IrisStorageError("Error storing data")

    def get_shared_json_data(self, shared_id):

        try:
            response = self.client.get_object(Bucket=iris_settings.IRIS_SESSION_BUCKET, Key="shared/" + shared_id)
            return json.loads(response['Body'].read())
        except ClientError:
            raise IrisStorageError("Error getting data")

    def expand_json_obj(self, obj):

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
