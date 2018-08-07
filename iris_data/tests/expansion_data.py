ID1 = "3a569cbc-49a3-4772-bf3d-3d46c4a51d32"

TEST_JSON_1 = {
    "name": "some_name",
    "values": [
        "value1", "value2"
    ]
}

SHARED_ID = "2d34bed8-c79a-4f90-b992-f7d3b5bc1308"

SHARED_JSON = {
    "shared_value": "psx"
}

EXPANSION_JSON = {

    "services": {
        "starsky": {
            "OCR": {
                "DPI": 200,
                "strategy": "GoogleVision"
            }
        },
        "montague": {
            "pipeline": "digi-arc"
        },
        "test": {
            "test_key": "test_value"
        }
    },
    "canvases": {
        "http://glam-dev.org/work/workx/canvas/0": {
            "services": {
                "starsky": {
                    "skip": True
                },
                "montague": {
                    "vision": "[[common:vision]]"
                },
                "test": [
                    {
                        "shared": "[[shared:" + SHARED_ID + "]]"
                    },
                    {
                        "notshared": "ps1"
                    }
                ]
            }
        }
    },
    "common": {
        "vision": {
            "vision_config": {
                "system": "x"
            }
        }
    }
}

EXPANDED_JSON = {

    "services": {
        "starsky": {
            "OCR": {
                "DPI": 200,
                "strategy": "GoogleVision"
            }
        },
        "montague": {
            "pipeline": "digi-arc"
        },
        "test": {
            "test_key": "test_value"
        }
    },
    "canvases": {
        "http://glam-dev.org/work/workx/canvas/0": {
            "services": {
                "starsky": {
                    "skip": True
                },
                "montague": {
                    "vision": {
                        "vision_config": {
                            "system": "x"
                        }
                    }
                },
                "test": [
                    {
                        "shared": {
                            "shared_value": "psx"
                        }
                    },
                    {
                        "notshared": "ps1"
                    }
                ]
            }
        }
    },
    "common": {
        "vision": {
            "vision_config": {
                "system": "x"
            }
        }
    }
}
