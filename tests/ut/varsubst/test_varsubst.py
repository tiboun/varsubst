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

from typing import Optional

from varsubst import varsubst
from varsubst.resolvers import BaseResolver

resolved_suffix = '_resolved'
unresolved_suffix = '_unresolved'
empty_suffix = '_empty'


class DummyResolver(BaseResolver):
    def resolve(self, key: str) -> Optional[str]:
        if key.endswith(unresolved_suffix):
            return None
        elif key.endswith(empty_suffix):
            return ''
        else:
            return key + resolved_suffix


def test_simple():
    test_fmt = 'foo {0} bar'
    expected = test_fmt.format('FOO' + resolved_suffix)
    test_str = test_fmt.format('$FOO')
    actual = varsubst(test_str, resolver=DummyResolver())
    assert actual == expected
