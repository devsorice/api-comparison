from enum import Enum, auto


class BackendFramewoks(Enum):
    RUST_AXUM       = auto()
    PYTHON_DJANGO   = auto()
    PYTHON_FLASK    = auto()
    PHP             = auto()
    NODE_JS_EXPRESS = auto()
