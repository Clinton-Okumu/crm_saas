from rest_framework.throttling import AnonRateThrottle

class LoginRateThrottle(AnonRateThrottle):
    """
    Throttle for login attempts
    """
    rate = '5/minute'