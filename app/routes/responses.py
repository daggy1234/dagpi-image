from pydantic import BaseModel
from typing import Union, Any, Dict


class Message(BaseModel):
    message: str


responses: Dict[Union[str, int], Dict[str, Any]] = {
    "404": {
        "message": Message,
        "content": {
            "application/json": {
                "example": ""
            }
        }
    },
    "415": {
        "message": Message,
        "content": {
            "application/json": {
                "example": {
                    "message": "No image found at your destination"
                },
                "example2": {
                    "message": "File found was not of Appropriate image type"
                }
            }
        }
    },
    "422": {
        "message": Message,
        "content": {
            "application/json": {
                "example": {
                    "message": "Unable to process the image due to an Error"
                }
            }
        }
    },
    "413": {
        "message": Message,
        "content": {
            "application/json": {
                "example": {
                    "message": "Image supplied was too large to be processed"
                }
            }
        }
    },
    "429": {
        "message": Message,
        "content": {
            "application/json": {
                "example": {
                    "message": "Ratelimited"
                }
            }
        }
    },
    "403": {
        "message": Message,
        "content": {
            "application/json": {
                "example": {
                    "message": "Unauthorised"
                }
            }
        }
    },
    "400": {
        "message": Message,
        "content": {
            "application/json": {
                "example": {
                    "message": "Unauthorised"
                }
            }
        }
    }
}

gif_response_only: Dict[Union[str, int], Dict[str, Any]] = {
    **responses,
    "200": {
        "message": Message,
        "content": {
            "image/gif": {}
        }
    },
}

static_response_only: Dict[Union[str, int], Dict[str, Any]] = {
    **responses,
    "200": {
        "message": Message,
        "content": {
            "image/png": {}
        }
    },
}

normal_response: Dict[Union[str, int], Dict[str, Any]] = {
    **responses,
    "200": {
        "message": Message,
        "content": {
            "image/gif": {},
            "image/png": {}
        }
    },
}
