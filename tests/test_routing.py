from src.routing import GraphRouter

def test_shortest_path_basic():
    gr = GraphRouter()
    gr.add_edge("A", "B", 5)
    gr.add_edge("B", "C", 2)
    gr.add_edge("A", "C", 10)
    cost, path = gr.shortest_path("A", "C")
    assert cost == 7
    assert path == ["A", "B", "C"]