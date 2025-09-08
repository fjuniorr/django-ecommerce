from collections import defaultdict
from typing import Type, Dict
from .adapter_key import AdapterKey

_REGISTRY: Dict[str, Type] = {}


def register(*keys: str):
    def deco(cls):
        for k in keys:
            _REGISTRY[k] = cls
        return cls
    return deco


def resolve(key_str: str) -> Type:
    key = AdapterKey.parse(key_str)
    for candidate in key.fallback_candidates():
        if candidate in _REGISTRY:
            return _REGISTRY[candidate]
    raise KeyError(key_str)
