from __future__ import annotations

from collections.abc import Callable
from typing import Any


class LocalJobQueue:
    """Queue abstraction.

    TODO: Replace local execution with Redis/Celery/RQ workers.
    """

    def enqueue(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)


job_queue = LocalJobQueue()
