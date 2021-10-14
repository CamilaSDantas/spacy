from typing import Protocol, runtime_checkable
from typing import Optional, Any, Iterable, Dict, Callable, Sequence, List

from thinc.api import Optimizer, Model


@runtime_checkable
class TrainableComponent(Protocol):
    model: Any
    is_trainable: bool

    def update(
        self,
        examples: Iterable["Example"],
        *,
        drop: float = 0.0,
        sgd: Optimizer = None,
        losses: Optional[Dict[str, float]] = None
    ) -> Dict[str, float]:
        ...

    def finish_update(self, sgd: Optimizer) -> None:
        ...


@runtime_checkable
class InitializableComponent(Protocol):
    def initialize(
        self,
        get_examples: Callable[[], Iterable["Example"]],
        nlp: Iterable["Example"],
        **kwargs: Any
    ):
        ...


@runtime_checkable
class ListenedToComponent(Protocol):
    model: Any
    listeners: Sequence[Model]
    listener_map: Dict[str, Sequence[Model]]
    listening_components: List[str]

    def add_listener(self, listener: Model, component_name: str) -> None:
        ...

    def remove_listener(self, listener: Model, component_name: str) -> bool:
        ...

    def find_listeners(self, component) -> None:
        ...
