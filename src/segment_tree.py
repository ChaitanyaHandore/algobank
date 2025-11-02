class SegmentTree:
    """
    Segment Tree supporting range add and point query.
    Demonstrates divide & conquer, tree recursion, and lazy propagation.
    """

    def __init__(self, n: int):
        self.cn = 1
        while self.cn < n:  # smallest power of 2 ≥ n
            self.cn <<= 1
        self.clazy = [0] * (2 * self.cn)

    def range_add(self, l: int, r: int, delta: int):
        """
        Add 'delta' to all elements in range [l, r] (inclusive).
        Time complexity: O(log n)
        """
        l += self.cn
        r += self.cn
        while l <= r:
            if l % 2 == 1:
                self.clazy[l] += delta
                l += 1
            if r % 2 == 0:
                self.clazy[r] += delta
                r -= 1
            l //= 2
            r //= 2

    def point_query(self, idx: int) -> int:
        """
        Query the accumulated value at position 'idx'.
        Time complexity: O(log n)
        """
        idx += self.cn
        res = 0
        while idx:
            res += self.clazy[idx]
            idx //= 2
        return res