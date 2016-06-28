class ConfigurationError(Exception):
    """
    This exception should be thrown if configuration errors happen
    """


class NotFoundError(Exception):
    """
    This exception should be thrown when a query by primary key returns nothing
    """
