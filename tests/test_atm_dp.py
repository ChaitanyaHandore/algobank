from src.atm_dp import min_notes

def test_min_notes_basic():
    assert min_notes(700, [500, 200, 100], [1, 5, 5]) == 2  # 500 + 200