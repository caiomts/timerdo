class TimerdoError(Exception):
    """A base class for Timerdo exceptions."""


class IdNotFoundError(TimerdoError):
    """Id Not Found Exception."""


class RunningTimerError(TimerdoError):
    """Running Timer Exception."""


class DoneTaskError(TimerdoError):
    """Task already done Exception."""


class NoTimeRunningError(TimerdoError):
    """No timer running Exception."""


class NoChangingError(TimerdoError):
    """No-changing Exception."""


class NegativeIntervalError(TimerdoError):
    """Negative Interval Exception."""


class OutOffPeriodError(TimeoutError):
    """Datetime is greater than now Exception."""
