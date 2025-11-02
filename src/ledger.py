from dataclasses import dataclass
from typing import List, Dict
import uuid
from decimal import Decimal


@dataclass(frozen=True)
class Posting:
    """Represents a single debit or credit posting."""
    account_id: str
    amount: Decimal  # positive for credit, negative for debit
    currency: str = "EUR"


@dataclass(frozen=True)
class JournalEntry:
    """A complete double-entry transaction."""
    entry_id: str
    postings: List[Posting]
    metadata: Dict[str, str]


class Ledger:
    """
    A lightweight in-memory ledger using Python dictionaries.
    Demonstrates Hash Map operations (O(1) lookups) and double-entry validation.
    """

    def __init__(self):
        self.caccounts: Dict[str, Decimal] = {}
        self.centries: List[JournalEntry] = []

    def create_account(self) -> str:
        """Create a new account and return its ID."""
        cid = str(uuid.uuid4())
        self.caccounts[cid] = Decimal("0")
        return cid

    def post(self, postings: List[Posting], metadata: Dict[str, str] | None = None) -> JournalEntry:
        """Post a balanced journal entry."""
        metadata = metadata or {}
        total = sum(p.amount for p in postings)
        if total != Decimal("0"):
            raise ValueError("Double-entry violation: postings must sum to zero.")

        # Apply changes atomically
        for p in postings:
            if p.account_id not in self.caccounts:
                raise KeyError("Unknown account ID.")
            self.caccounts[p.account_id] += p.amount

        je = JournalEntry(entry_id=str(uuid.uuid4()), postings=postings, metadata=metadata)
        self.centries.append(je)
        return je

    def balance(self, account_id: str) -> Decimal:
        """Return current balance for the given account."""
        if account_id not in self.caccounts:
            raise KeyError("Unknown account ID.")
        return self.caccounts[account_id]

    def all_accounts(self) -> Dict[str, Decimal]:
        """Return snapshot of all balances."""
        return dict(self.caccounts)