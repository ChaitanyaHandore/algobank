# 🏦 AlgoBank — Advanced DSA-Driven Banking Simulation

**AlgoBank** is a full-stack data-structures-and-algorithms project that simulates a digital banking ecosystem.  
It integrates real-world problems — transaction routing, fraud detection, ledger integrity, and interest accrual —  
solved using *advanced DSA techniques*.

---

## 🚀 Features & Algorithms

| Feature | DSA Concept | Description |
|----------|--------------|-------------|
| 💸 **ATM Optimizer** | Dynamic Programming | Determines minimum number of notes to dispense efficiently. |
| 🧾 **Ledger System** | Hash Maps | Real-time O(1) balance lookups and double-entry validation. |
| 🌲 **Transaction Integrity** | Merkle Tree | Cryptographic proof of transaction history authenticity. |
| 💰 **Interest Engine** | Segment Tree | Efficient range updates and point queries in O(log n). |
| 🕵️ **Fraud Detection** | Disjoint Set Union | Identifies connected clusters of suspicious accounts. |
| 🌐 **Routing System** | Dijkstra’s Algorithm | Computes least-cost path between banks using a priority queue. |

---

## 🧠 Tech Stack
- **Language:** Python 3.12  
- **Testing:** Pytest  
- **Algorithms:** Graphs, DP, Trees, Union-Find, HashMaps  
- **Complexity:** O(E log V) (routing) | O(log n) (segment updates) | O(α(n)) (fraud union)

---

## 🧪 Run Locally
```bash
git clone https://github.com/ChaitanyaHandore/algobank.git
cd algobank/AlgoBank
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -v       # run all tests
python3 -m src.main   # run full simulation