# strategies/__init__.py

from .exit_strategy import evaluate_exit_conditions
from .trailing_stop import should_exit_trailing

__all__ = [
    "evaluate_exit_conditions",
    "should_exit_trailing"
]