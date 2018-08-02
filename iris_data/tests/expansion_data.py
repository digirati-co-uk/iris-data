SHARED_ID = "2d34bed8-c79a-4f90-b992-f7d3b5bc1308"

SHARED_JSON = {
    "shared_value": "psx"
}

EXPANSION_JSON = {
    "manifest": "http://glam-dev.org/work/workx",
    "services": {
        "starsky": {
            "OCR": {
                "DPI": 200,
                "strategy": "GoogleVision"
            }
        },
        "montague": {
            "pipeline": "digi-arc"
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
    "manifest": "http://glam-dev.org/work/workx",
    "services": {
        "starsky": {
            "OCR": {
                "DPI": 200,
                "strategy": "GoogleVision"
            }
        },
        "montague": {
            "pipeline": "digi-arc"
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
