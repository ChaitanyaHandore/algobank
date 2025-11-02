class DSU:
    """
    Disjoint Set Union (Union-Find) for clustering accounts.
    Used to detect whether two accounts are connected directly or indirectly.
    """

    def __init__(self):
        self.cpar = {}
        self.crank = {}

    def add(self, x):
        """Add a new element to the DSU if not present."""
        if x not in self.cpar:
            self.cpar[x] = x
            self.crank[x] = 0

    def find(self, x):
        """Find the root representative of x with path compression."""
        if self.cpar[x] != x:
            self.cpar[x] = self.find(self.cpar[x])
        return self.cpar[x]

    def union(self, a, b):
        """Union two sets (a, b). Returns True if merged, False if already in same set."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.crank[ra] < self.crank[rb]:
            ra, rb = rb, ra
        self.cpar[rb] = ra
        if self.crank[ra] == self.crank[rb]:
            self.crank[ra] += 1
        return True

    def connected(self, a, b) -> bool:
        """Check if two elements are in the same set."""
        if a not in self.cpar or b not in self.cpar:
            return False
        return self.find(a) == self.find(b)