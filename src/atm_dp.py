# Minimum number of notes to make amount with limited note counts (bounded knapsack)
def min_notes(amount: int, notes: list[int], counts: list[int]) -> int:
    INF = 10**9
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for denom, cnt in zip(notes, counts):
        k = 1
        c = cnt
        # binary splitting of counts
        while c > 0:
            take = min(k, c)
            val = take * denom
            for s in range(amount, val - 1, -1):
                if dp[s - val] + take < dp[s]:
                    dp[s] = dp[s - val] + take
            c -= take
            k <<= 1
    return dp[amount] if dp[amount] < INF else -1