from abc import ABC, abstractmethod

class AbstractPage(ABC):
    @abstractmethod
    def process_form(self, form: object, is_multiple: bool=True) -> dict:
        pass
