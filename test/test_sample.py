from app.sample import *
import pytest

@pytest.mark.parametrize('num1, num2, result', [
    (2, 3, 5),
    (2, -3, -1),
    (-2, -3, -5),
    (-2, 0, -2),
    (2, 0, 2),
])

def test_add(num1, num2, result):
    assert add(num1, num2) == result

@pytest.fixture
def bank_account():
    return BankAccount()

def test_bank_account(bank_account):
    bank_account.deposit(200)
    bank_account.withdraw(100)
    assert round(bank_account.balance, 4) == 100

def test_raise_exception(bank_account):
    with pytest.raises(ValueError):
        bank_account.withdraw(100)