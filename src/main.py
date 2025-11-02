from decimal import Decimal
from src.ledger import Ledger, Posting
from src.merkle import hex_root
from src.routing import GraphRouter
from src.segment_tree import SegmentTree
from src.fraud_graph import DSU
from src.atm_dp import min_notes


def demo_algobank():
    print("\n🏦  Welcome to AlgoBank Simulation\n")

    # --- Ledger setup ---
    ledger = Ledger()
    acc1 = ledger.create_account()
    acc2 = ledger.create_account()

    ledger.post([
        Posting(acc1, Decimal("-500")),
        Posting(acc2, Decimal("500")),
    ], metadata={"desc": "Initial deposit"})

    print(f"Account {acc1[:6]} balance:", ledger.balance(acc1))
    print(f"Account {acc2[:6]} balance:", ledger.balance(acc2))

    # --- Merkle Tree for transaction integrity ---
    entries = [b"tx1:500EUR", b"tx2:200EUR", b"tx3:100EUR"]
    print("\nMerkle Root for transactions:", hex_root(entries))

    # --- Segment Tree for interest accrual simulation ---
    st = SegmentTree(5)
    st.range_add(0, 4, 1)
    st.range_add(2, 3, 2)
    print("\nSegment Tree interest check → Day3 interest:", st.point_query(3))

    # --- Fraud network detection using DSU ---
    fraud = DSU()
    for acc in [acc1, acc2, "ghost1", "ghost2"]:
        fraud.add(acc)
    fraud.union(acc1, "ghost1")
    print("\nFraud link check:", fraud.connected(acc1, "ghost1"))

    # --- Routing between banks using Dijkstra ---
    router = GraphRouter()
    router.add_edge("BankA", "BankB", 3)
    router.add_edge("BankB", "BankC", 2)
    router.add_edge("BankA", "BankC", 10)
    cost, path = router.shortest_path("BankA", "BankC")
    print("\nCheapest route from BankA → BankC:", path, "Cost:", cost)

    # --- ATM DP optimizer ---
    notes = [500, 200, 100]
    counts = [2, 5, 10]
    amount = 700
    print(f"\nMin notes to withdraw {amount}:", min_notes(amount, notes, counts))

    print("\n✅ AlgoBank simulation complete!\n")


if __name__ == "__main__":
    demo_algobank()