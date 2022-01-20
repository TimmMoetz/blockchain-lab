from .message import Message

class Vote(Message):
    def __init__(self, transaction, valid) -> None:
        super().__init__()
        self._name = "vote"
        self._transaction = transaction
        self._valid = valid

    def get_transaction(self):
        return self._transaction

    def set_transaction(self, transaction):
        self._transaction = transaction 

    def get_valid(self):
        return self._valid

    def set_valid(self, valid):
        self._valid = valid

    def to_dict(self):
        return {
            "name": self.get_name(),
            "transaction": self.get_transaction(),
            "valid": self.get_valid(),
        }

    @staticmethod
    def from_dict(dict):
        return Vote(dict["transaction"], dict["valid"])
       
