
class DuplicateTrackingInformation(Exception):
    """user and flight already registered in database"""
    pass

class InvalidCell(Exception):
    """user cell cannot be validated"""
    pass

class MissingFlight(Exception):
    """cannot find flight"""
    pass
