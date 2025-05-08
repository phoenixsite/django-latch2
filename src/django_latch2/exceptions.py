"""
Exception classes used in Latch operations.
"""

# SPDX-License-Identifier: BSD-3-Clause


class BaseLatchError(Exception):
    """
    Base class for errors during latch operation.
    """

    def __init__(self, message, code=None, params=None):
        super().__init__(message, code, params)
        self.message = message
        self.code = code
        self.params = params


class PairingLatchError(BaseLatchError):
    """
    Class for errors during latch's pairing.
    """


class UnpairingLatchError(BaseLatchError):
    """
    Class for errors during latch's unpairing.
    """
