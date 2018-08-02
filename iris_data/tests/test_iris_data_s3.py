import pytest
import boto3
import json
import iris_settings
from moto import mock_s3

from iris_data.tests import expansion_data
from iris_data.iris_data_s3 import IrisSession


BUCKET = "iris_moto_bucket"
ID1 = "3a569cbc-49a3-4772-bf3d-3d46c4a51d32"


TEST_JSON_1 = {
    "name": "some_name",
    "values": [
        "value1", "value2"
    ]
}


@pytest.fixture()
def moto_boto():

    # start moto
    mock_s3().start()
    resource = boto3.resource('s3')
    client = boto3.client('s3')
    resource.create_bucket(Bucket=iris_settings.IRIS_SESSION_BUCKET)

    # yield
    yield client, resource

    # shutdown mono
    mock_s3().stop()


def test_store_shared_data(moto_boto):

    # setup
    test_content = json.dumps(TEST_JSON_1)

    # run test
    session = IrisSession()
    session.store_shared_data(ID1, test_content)

    # check result
    key_name = "shared/" + ID1
    s3 = moto_boto[1]
    bucket = s3.Bucket(iris_settings.IRIS_SESSION_BUCKET)
    keys = list(bucket.objects.filter(Prefix=key_name))
    assert len(keys) == 1
    assert keys[0].key == key_name
    key = s3.Object(iris_settings.IRIS_SESSION_BUCKET, key_name).get()
    key_content = key['Body'].read().decode()
    assert test_content == key_content


def test_store_shared_json_data(moto_boto):

    # run test
    session = IrisSession()
    session.store_shared_json_data(ID1, TEST_JSON_1)

    # check result
    key_name = "shared/" + ID1
    s3 = moto_boto[1]
    bucket = s3.Bucket(iris_settings.IRIS_SESSION_BUCKET)
    keys = list(bucket.objects.filter(Prefix=key_name))
    assert len(keys) == 1
    assert keys[0].key == key_name
    key = s3.Object(iris_settings.IRIS_SESSION_BUCKET, key_name).get()
    key_content = key['Body'].read().decode()
    assert json.dumps(TEST_JSON_1) == key_content


def test_store_retrieve_shared_data(moto_boto):

    # setup
    test_content = json.dumps(TEST_JSON_1)

    # run test
    session = IrisSession()
    session.store_shared_data(ID1, test_content)

    # check result
    result = session.get_shared_data(ID1)

    # result will be byte array
    assert result.decode() == test_content


def test_store_retrieve_shared_json_data(moto_boto):

    # setup
    test_content = json.dumps(TEST_JSON_1)

    # run test
    session = IrisSession()
    session.store_shared_json_data(ID1, test_content)

    # check result
    result = session.get_shared_json_data(ID1)

    assert result == test_content

def test_store_retrieve_data(moto_boto):

    # setup
    test_content = json.dumps(TEST_JSON_1)

    # run test
    session = IrisSession()
    session.store_data(ID1, test_content)

    # check result
    result = session.get_data(ID1)

    # result will be byte array
    assert result.decode() == test_content


def test_store_retrieve_json_data(moto_boto):

    # setup
    test_content = json.dumps(TEST_JSON_1)

    # run test
    session = IrisSession()
    session.store_json_data(ID1, test_content)

    # check result
    result = session.get_json_data(ID1)

    assert result == test_content


def test_expand_json(moto_boto):

    session = IrisSession()
    session.store_shared_json_data(expansion_data.SHARED_ID, expansion_data.SHARED_JSON)
    expanded_data = session.expand_json_obj(expansion_data.EXPANSION_JSON)
    assert expanded_data == expansion_data.EXPANDED_JSON
