# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2020 Bounkong Khamphousone
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and
# this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import environ
from typing import Any, Dict, Optional


class BaseResolver:
    """
    Abstract base class for all resolvers. Don't instantiate it.

    A resolver is intented to provide values from keys.
    """

    def resolve(self, key: str) -> Optional[Any]:
        """
        Resolver should be able to produce a value for a given key.
        If key doesn't exist, should return None.
        """
        pass

    def values(self) -> Dict[str, Any]:
        """
        Return all values available in the resolver.
        """
        pass


class EnvResolver(BaseResolver):
    """
    EnvResolver provide a value based on environnement variables.
    """

    def resolve(self, key: str) -> Optional[Any]:
        """
        Resolver should be able to produce a value for a given key.
        If key doesn't exist, should return None.
        """
        return environ.get(key)

    def values(self) -> Dict[str, Any]:
        return environ.copy()


class DictResolver(BaseResolver):
    """
    DictResolver provide a value based on a given dictionary.
    """

    def __init__(self, dict: Dict[str, Any]) -> None:
        """
        :param dict: dictionary used to resolve given keys
        """
        self.dict = dict

    def resolve(self, key: str) -> Optional[Any]:
        """
        Resolver should be able to produce a value for a given key.
        If key doesn't exist, should return None.
        """
        return self.dict.get(key)

    def values(self) -> Dict[str, Any]:
        """
        Return all values available in the resolver.
        """
        return self.dict.copy()
