from pydantic import BaseModel
from typing import Union, Any, Dict


class Message(BaseModel):
    message: str


responses: Dict[Union[str, int], Dict[str, Any]] = {
    "404": {
        "model": Message,
        "content": {
            "application/json": {
                "example": ""
            }
        }
    },
    "415": {
        "model": Message,
        "content": {
            "application/json": {
                "example": {
                    "model": "No image found at your destination"
                },
                "example2": {
                    "model": "File found was not of Appropriate image type"
                }
            }
        }
    },
    "422": {
        "model": Message,
        "content": {
            "application/json": {
                "example": {
                    "model": "Unable to process the image due to an Error"
                }
            }
        }
    },
    "413": {
        "model": Message,
        "content": {
            "application/json": {
                "example": {
                    "model": "Image supplied was too large to be processed"
                }
            }
        }
    },
    "429": {
        "model": Message,
        "content": {
            "application/json": {
                "example": {
                    "model": "Ratelimited"
                }
            }
        }
    },
    "403": {
        "model": Message,
        "content": {
            "application/json": {
                "example": {
                    "model": "Unauthorised"
                }
            }
        }
    },
    "400": {
        "model": Message,
        "content": {
            "application/json": {
                "example": {
                    "model": "Unauthorised"
                }
            }
        }
    }
}

gif_response_only: Dict[Union[str, int], Dict[str, Any]] = {
    **responses,
    "200": {
        "model": Message,
        "content": {
            "image/gif": {}
        }
    },
}

static_response_only: Dict[Union[str, int], Dict[str, Any]] = {
    **responses,
    "200": {
        "model": Message,
        "content": {
            "image/png": {}
        }
    },
}

normal_response: Dict[Union[str, int], Dict[str, Any]] = {
    **responses,
    "200": {
        "model": Message,
        "content": {
            "image/gif": {},
            "image/png": {}
        }
    },
}
