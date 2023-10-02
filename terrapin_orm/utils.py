import uuid
from collections.abc import Callable
from typing import Any

import orjson


def convertor(obj: Any) -> Any:
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def orjson_dumps(v: Any, /, *, default: Callable[[Any], Any] = convertor) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()
