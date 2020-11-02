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

import re
from typing import AnyStr, Pattern

from varsubst.exceptions import KeyUnresolvedException
from varsubst.resolvers import BaseResolver


class BaseInterpolator:
    """
    Abstract base class for all interpolators. Don't instantiate it.

    An interpolator is intented to render a template with values
    provided by a resolver.
    """

    def render(self, template: str, resolver: BaseResolver) -> str:
        """
        :param template: String with shell-like variables.
            Allowed variables are of the form:
                - $MY_SIMPLE_VAR
                - ${MY_SIMPLE_VAR}
                - ${USER-default}
                - ${USER-$DEFAULT_USER}
                - ${USER:-default}
                - ${USER-$DEFAULT_USER}
        """
        pass


class ShellInterpolator(BaseInterpolator):

    _simple_re: Pattern[AnyStr] = re.compile(r'(?<!\\)\$([A-Za-z0-9_]+)')
    """
    For a given string, will match ${anystring1:-anystring2} or
    ${anystring1-anystring2}

    Groups extracted are :
        1. anystring1
        2. :-anystring2 or -anystring2
        3. :- or -
        4. anystring2
    """
    _extended_re: Pattern[AnyStr] = re.compile(
        r'(?<!\\)\$\{([A-Za-z0-9_]+)((:?-)([^}]+))?\}')

    def __init__(self, fail_on_unresolved: bool) -> None:
        """
        :param fail_on_unresolved: if true, will throw an exception.
        """
        self.fail_on_unresolved = fail_on_unresolved

    def _repl_simple_env_var(self, resolver: BaseResolver) -> str:
        """
        :param resolver: an instance which return a value given a key
        """
        def substitute(m):
            var_name = m.group(1)
            result = resolver.resolve(var_name)
            if result is None and self.fail_on_unresolved:
                raise KeyUnresolvedException(var_name)
            return result or ''

        return substitute

    def _repl_extended_env_var(self, resolver: BaseResolver) -> str:
        """
        :param resolver: an instance which return a value given a key
        """
        def substitute(m):
            var_name = m.group(1)
            result = resolver.resolve(var_name)
            default_spec = m.group(2)
            if default_spec:
                default_raw = m.group(4)
                if m.group(3) == ':-':
                    # use default if var is unset or empty
                    if not result:
                        result = ShellInterpolator._simple_re.sub(
                            self._repl_simple_env_var(resolver),
                            default_raw)
                elif m.group(3) == '-':
                    # use default if var is unset
                    if result is None:
                        result = ShellInterpolator._simple_re.sub(
                            self._repl_simple_env_var(resolver),
                            default_raw)
                else:
                    raise RuntimeError('Unexpected string matched regex')
            else:
                if result is None and self.fail_on_unresolved:
                    raise KeyUnresolvedException(var_name)
            return result or ''

        return substitute

    def render(self, template: str, resolver: BaseResolver) -> str:
        """
        Substitute shell like variables in the given template
        The following forms are supported:
        Simple variables - will use an empty string if the variable is unset
        $FOO
        Bracketed expressions
        ${FOO}
            identical to $FOO
        ${FOO:-somestring}
            uses "somestring" if $FOO is unset, or set and empty
        ${FOO-somestring}
            uses "somestring" only if $FOO is unset
        :param str string: A string possibly containing environment variables
        :return: The string with env variable specs replaced with their values
        """
        # handle simple un-bracketed env vars like $FOO
        first_pass = ShellInterpolator._simple_re.sub(
            self._repl_simple_env_var(resolver),
            template)

        # handle bracketed env vars with optional default specification
        return ShellInterpolator._extended_re.sub(
            self._repl_extended_env_var(resolver),
            first_pass)


class JinjaInterpolator(BaseInterpolator):

    def render(self, template: str, resolver: BaseResolver) -> str:
        """
        Substitute template using jinja.
        """
        from jinja2 import Template
        jtemplate = Template(template)
        return jtemplate.render(**resolver.values())
