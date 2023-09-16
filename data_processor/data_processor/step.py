from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple


class Step(ABC):
    def __init__(self, next_step: Optional["Step"] = None) -> None:
        self.next_step: Optional[Step] = next_step

    def __call__(self, *data: Tuple) -> Any:
        processed_data: Tuple = self.process(*data)
        self.send_to_next_step(processed_data)

    @abstractmethod
    def process(self, *data: Tuple) -> Tuple:
        pass

    def send_to_next_step(self, data: Tuple):
        if self.next_step:
            self.next_step(*data)
