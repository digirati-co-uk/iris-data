import pytest
import boto3
import json
import iris_settings
from moto import mock_s3

from iris_data.exceptions import IrisStorageError
from iris_data.tests import expansion_data
from iris_data.iris_data_s3 import IrisSessionData


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


@pytest.fixture()
def broken_moto_boto():

    # start moto
    mock_s3().start()
    resource = boto3.resource('s3')
    client = boto3.client('s3')

    # resource.create_bucket(Bucket=iris_settings.IRIS_SESSION_BUCKET)

    # yield
    yield client, resource

    # shutdown mono
    mock_s3().stop()



def test_store_shared_json_data(moto_boto):

    # run test
    session = IrisSessionData()
    session.store_shared_json_data(expansion_data.ID1, expansion_data.TEST_JSON_1)

    # check result
    key_name = "shared/" + expansion_data.ID1
    s3 = moto_boto[1]
    bucket = s3.Bucket(iris_settings.IRIS_SESSION_BUCKET)
    keys = list(bucket.objects.filter(Prefix=key_name))
    assert len(keys) == 1
    assert keys[0].key == key_name
    key = s3.Object(iris_settings.IRIS_SESSION_BUCKET, key_name).get()
    key_content = key['Body'].read().decode()
    assert json.dumps(expansion_data.TEST_JSON_1) == key_content


def test_store_retrieve_shared_json_data(moto_boto):

    # setup
    test_content = json.dumps(expansion_data.TEST_JSON_1)

    # run test
    session = IrisSessionData()
    session.store_shared_json_data(expansion_data.ID1, test_content)

    # check result
    result = session.get_shared_json_data(expansion_data.ID1)

    assert result == test_content


def test_store_retrieve_json_data(moto_boto):

    session = IrisSessionData()
    session.store_json_data(expansion_data.ID1, expansion_data.TEST_JSON_1)

    # check result
    result = session.get_json_data(expansion_data.ID1)

    assert result == expansion_data.TEST_JSON_1


def test_expand_json(moto_boto):

    session = IrisSessionData()
    session.store_shared_json_data(expansion_data.SHARED_ID, expansion_data.SHARED_JSON)
    expanded_data = session.expand_json_obj(expansion_data.EXPANSION_JSON)
    assert expanded_data == expansion_data.EXPANDED_JSON


def test_missing_bucket_shared(broken_moto_boto):

    session = IrisSessionData()
    with pytest.raises(IrisStorageError):
        session.store_shared_json_data(expansion_data.SHARED_ID, expansion_data.SHARED_JSON)


def test_missing_bucket(broken_moto_boto):

    session = IrisSessionData()
    with pytest.raises(IrisStorageError):
        session.store_json_data(expansion_data.SHARED_ID, expansion_data.EXPANSION_JSON)


def test_missing_key(moto_boto):

    # setup
    test_content = json.dumps(expansion_data.TEST_JSON_1)

    # run test
    session = IrisSessionData()
    session.store_shared_json_data(expansion_data.ID1, test_content)

    # check result
    with pytest.raises(IrisStorageError):
        session.get_shared_json_data(expansion_data.ID1 + "x")


def test_bad_session(moto_boto):

    # run test
    session = IrisSessionData()
    session.store_data(expansion_data.ID1, "test")

    # check result
    with pytest.raises(IrisStorageError):
        session.get_data(expansion_data.ID1 + "x")
