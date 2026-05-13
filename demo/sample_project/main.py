"""Simple Calculator API — demo project for DocFlow."""

import math
from typing import Optional


class Calculator:
    """A basic calculator with history tracking."""

    def __init__(self):
        self.history: list[dict] = []

    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self._record("add", a, b, result)
        return result

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        result = a - b
        self._record("subtract", a, b, result)
        return result

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        result = a * b
        self._record("multiply", a, b, result)
        return result

    def divide(self, a: float, b: float) -> float:
        """Divide a by b. Raises ValueError if b is zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self._record("divide", a, b, result)
        return result

    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent."""
        result = math.pow(base, exponent)
        self._record("power", base, exponent, result)
        return result

    def sqrt(self, value: float) -> float:
        """Calculate the square root of a value."""
        if value < 0:
            raise ValueError("Cannot compute square root of negative number")
        result = math.sqrt(value)
        self._record("sqrt", value, 0, result)
        return result

    def get_history(self) -> list[dict]:
        """Return the calculation history."""
        return self.history.copy()

    def clear_history(self) -> None:
        """Clear the calculation history."""
        self.history.clear()

    def _record(self, op: str, a: float, b: float, result: float) -> None:
        self.history.append({
            "operation": op,
            "operands": [a, b],
            "result": result,
        })


def create_calculator() -> Calculator:
    """Factory function to create a Calculator instance."""
    return Calculator()
