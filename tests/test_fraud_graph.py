from src.fraud_graph import DSU

def test_dsu_basic():
    dsu = DSU()
    dsu.add("A")
    dsu.add("B")
    dsu.add("C")
    dsu.union("A", "B")
    assert dsu.connected("A", "B") is True
    assert dsu.connected("A", "C") is False