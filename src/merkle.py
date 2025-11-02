import hashlib
from typing import Iterable

def _h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def leaf_hash(entry_bytes: bytes) -> bytes:
    return _h(b"\x00" + entry_bytes)

def node_hash(left: bytes, right: bytes) -> bytes:
    return _h(b"\x01" + left + right)

def merkle_root(leaves: Iterable[bytes]) -> bytes:
    layer = [leaf_hash(x) for x in leaves]
    if not layer:
        return _h(b"")
    while len(layer) > 1:
        nxt = []
        if len(layer) % 2 == 1:
            layer.append(layer[-1])        # duplicate last if odd count
        for i in range(0, len(layer), 2):
            nxt.append(node_hash(layer[i], layer[i + 1]))
        layer = nxt
    return layer[0]

def hex_root(leaves: Iterable[bytes]) -> str:
    return merkle_root(leaves).hex()