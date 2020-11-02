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

import os
from typing import Optional

import pytest

from varsubst.exceptions import KeyUnresolvedException
from varsubst.interpolators import ShellInterpolator
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
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_bracketed_simple():
    test_fmt = 'foo {0} bar'
    expected = test_fmt.format('FOO' + resolved_suffix)
    test_str = test_fmt.format('${FOO}')
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_unset_default():
    test_fmt = 'abc {0} def'
    default_str = 'i am a default'
    test_var = '${FOO' + unresolved_suffix + '-' + default_str + '}'
    test_str = test_fmt.format(test_var)
    expected = test_fmt.format(default_str)
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_unset_only_no_default():
    test_val = ''
    test_fmt = 'abc {0} def'
    default_str = 'i am a default'
    test_var = '${FOO' + empty_suffix + '-' + default_str + '}'
    test_str = test_fmt.format(test_var)
    expected = test_fmt.format(test_val)
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_no_default_with_unset_only_operator():
    test_fmt = 'abc {0} def'
    test_var = '${FOO-i am a default}'
    test_str = test_fmt.format(test_var)
    expected = test_fmt.format('FOO' + resolved_suffix)
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_empty_unset_or_empty_default():
    test_fmt = 'abc {0} def'
    default_str = 'i am a default'
    test_var = '${FOO' + empty_suffix + ':-' + default_str + '}'
    test_str = test_fmt.format(test_var)
    expected = test_fmt.format(default_str)
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_unset_unset_or_empty_default():
    test_fmt = 'abc {0} def'
    default_str = 'i am a default'
    test_var = '${FOO' + unresolved_suffix + ':-' + default_str + '}'
    test_str = test_fmt.format(test_var)
    expected = test_fmt.format(default_str)
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_no_default_with_emtpy_operator():
    test_fmt = 'abc {0} def'
    test_var = '${FOO:-i am a default}'
    test_str = test_fmt.format(test_var)
    expected = test_fmt.format('FOO' + resolved_suffix)
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_multiple():
    try:
        del os.environ['NOPE']
    except KeyError:
        pass

    nope_default = 'var NOPE not there'

    test_fmt = 'abc {0} def {1}{2} jkl {3} mno'
    test_str = test_fmt.format(
        '$FOO',
        '${BAR}',
        '${BAR2:-default for bar2}',
        '${NOPE' + unresolved_suffix + '-' + nope_default + '}',
    )
    expected = test_fmt.format(
        'FOO' + resolved_suffix,
        'BAR' + resolved_suffix,
        'BAR2' + resolved_suffix,
        nope_default
    )
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_escaped():
    tests = [
        r'i am an \$ESCAPED variable',
        r'i am an \${ESCAPED:-bracketed} \${expression}',
    ]
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    for test in tests:
        assert test == interpolator.render(test, resolver=DummyResolver())


def test_simple_var_default():
    test_fmt = 'abc {0} def'
    test_str = test_fmt.format('${TEST' + empty_suffix + ':-$DEFAULT}')
    expected = test_fmt.format('DEFAULT' + resolved_suffix)
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected


def test_unresolved_key_exception():
    test_fmt = 'abc {0} def'
    test_str = test_fmt.format('$FOO' + unresolved_suffix)
    interpolator = ShellInterpolator(fail_on_unresolved=True)
    with pytest.raises(KeyUnresolvedException):
        interpolator.render(test_str, resolver=DummyResolver())


def test_unresolved_key_fallback():
    test_fmt = 'abc {0} def'
    test_str = test_fmt.format('$FOO' + unresolved_suffix)
    expected = test_fmt.format('')
    interpolator = ShellInterpolator(fail_on_unresolved=False)
    actual = interpolator.render(test_str, resolver=DummyResolver())
    assert actual == expected
