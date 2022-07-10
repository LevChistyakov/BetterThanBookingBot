class ResponseIsEmptyError(BaseException):
    """Request to rapidapi doesn't return anything"""

    def __str__(self):
        return 'Server returned None'
