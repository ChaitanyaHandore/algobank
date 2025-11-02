from src.ledger import Ledger, Posting
from decimal import Decimal

def test_post_balanced():
    led = Ledger()
    a1, a2 = led.create_account(), led.create_account()
    led.post([
        Posting(a1, Decimal("-100")),
        Posting(a2, Decimal("100"))
    ])
    assert led.balance(a1) == Decimal("-100")
    assert led.balance(a2) == Decimal("100")