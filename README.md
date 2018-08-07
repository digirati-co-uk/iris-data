# Iris Session Data Library

This library provides a simple session data storage system, designed for event driven workflows built on the Iris Message Bus project. 

Currently an AWS S3 backed implementation is provided and there is a dependency on S3 to use this. 

### Installation


* (optional: create virtual environment)
* ``` pip install -r requirements.txt ```
* create or edit iris_settings.py including an "IRIS_SESSION_BUCKET" property


### example usage

```python
    from iris_data.iris_data_s3 import IrisSessionData
    
    # create
    session = IrisSessionData()
    
    # store
    session.store_json_data(ID1, TEST_JSON_1)

    # retrieve
    result = session.get_json_data(ID1)
```

