from abc import ABC, abstractmethod
from typing import Iterable, Any


class BaseRepository[Obj, ID](ABC):
    @abstractmethod
    async def get_all(
        self, offset: int = None, limit: int = None, **filters: Any
    ) -> Iterable[Obj]: ...

    @abstractmethod
    async def get(self, id_obj: ID) -> Obj: ...

    @abstractmethod
    async def create(self, create_dict: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id_obj: ID) -> None: ...

    @abstractmethod
    async def update(self, obj: Obj, update_dict: dict[str, Any]) -> None: ...
