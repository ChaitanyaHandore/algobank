from src.merkle import hex_root

def test_merkle_basic():
    h = hex_root([b"txn1", b"txn2", b"txn3"])
    assert isinstance(h, str)
    assert len(h) == 64