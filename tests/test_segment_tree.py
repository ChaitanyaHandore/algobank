from src.segment_tree import SegmentTree

def test_segment_tree_range_add_point_query():
    st = SegmentTree(10)
    st.range_add(0, 9, 1)
    st.range_add(2, 4, 2)
    assert st.point_query(3) == 3   # 1 + 2
    assert st.point_query(8) == 1