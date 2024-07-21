"""mongoengine Mock"""
from typing import Any


class BogusMongo:
    """Mock MongoEngine"""

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        """Mock mongoengine.connect(arg)"""
        pass

    def __getitem__(self, _key: str) -> Any:
        """Mock getitem"""
        return self

    def objects(self, *_args: Any, **_kwargs: Any) -> Any:
        """Mock mongoengine query"""
        return self

    def update(self, *_args: Any, **_kwargs: Any) -> Any:
        """Mock mongoengine update"""
        pass

    def rollback(self, *_args: Any, **_kwargs: Any) -> None:
        """Mock Rollback"""
        pass

    def __enter__(self, *_args: Any, **_kwargs: Any) -> Any:
        """Mock __enter__"""
        return self

    def __exit__(self, *_args: Any, **_kwargs: Any) -> Any:
        """Mock __exit__"""
        pass
