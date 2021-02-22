class BaseException(Exception):

    def __init__(self, msg):
        self.msg = msg


class AccountNotFoundException(BaseException):
    pass


class BalanceIsClosedException(BaseException):
    pass


class InsufficientFundsException(BaseException):
    pass
