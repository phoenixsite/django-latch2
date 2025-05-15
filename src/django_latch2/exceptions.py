"""
Exception classes used in Latch operations.
"""

# SPDX-License-Identifier: BSD-3-Clause


class BaseLatchError(Exception):
    """
    Base class for errors during latch operation.

    This exception will not be raised anywhere, it just serves
    as a base for the other two exception types.

    :param str message: A human-readable error message.
    :param str code: A unique identifier used to distinguish different
            error causes.
    :param dict params: Arbitrary key-value data associated with the error.
    """

    def __init__(self, message, code=None, params=None):
        super().__init__(message, code, params)
        self.message = message
        self.code = code
        self.params = params


class PairingLatchError(BaseLatchError):
    """
    Exception class to indicate errors during latch's pairing.
    """


class UnpairingLatchError(BaseLatchError):
    """
    Exception class to indicate errors during latch's unpairing.
    """
