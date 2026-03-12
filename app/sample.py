def add(num1: int, num2: int) -> int:
    return num1 + num2

class BankAccount:
    INTEREST_RATE = 0.10

    def __init__(self, initial_amount: float = 0.0) -> None:
        if initial_amount < 0:
            raise ValueError("Initial amount cannot be negative")
        self.balance: float = initial_amount

    def withdraw(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Withdraw amount cannot be negative")
        if amount > self.balance:
            raise ValueError("Insufficient balance")

        self.balance -= amount

    def deposit(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Deposit amount cannot be negative")

        self.balance += amount

    def with_interest(self) -> float:
        return self.balance * (1 + self.INTEREST_RATE)