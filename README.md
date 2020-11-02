![Tests](https://github.com/tiboun/varsubst/workflows/tests/badge.svg)

Varsubst is a rewrite of [envsubst](https://github.com/ashafer01/python-envsubst).

Varsubst render templates from a string with a given resolver.

Currently varsubst support shell-like variables.

Entry-point has currently been removed. It may be added in the future.

Resolvers provided are :
- **EnvResolver** : provide value based on environnement variables.
- **DictResolver** : provide value based on a given python dictionary.

# Supported template variables

Varsubst support shell-like variables which are defined as follows:
- **$MY_SIMPLE_VAR** or **${MY_SIMPLE_VAR}**: will resolve the variable *MY_SIMPLE_VAR*
- **${USER-default}** : will resolve the variable *USER*. If variable is unset then *default* string is returned.
- **${USER-$DEFAULT_USER}** : will resolve the variable *USER*. If variable is unset, resolve the variable *DEFAULT_USER*.
- **${USER:-default}** : will resolve the variable *USER*. If variable is unset or empty then *default* string is returned.
- **${USER-$DEFAULT_USER}** : will resolve the variable *USER*. If variable is unset or empty, resolve the variable *DEFAULT_USER*.

# Usage

```python
from varsubst import varsubst
from varsubst.resolvers import DictResolver
from varsubst.interpolators import JinjaInterpolator

print(varsubst('$USER')) # result : 'tiboun'

print(varsubst('$UNDEFINED')) # result : KeyUnresolvedException('UNDEFINED')

print(varsubst('$UNDEFINED', fail_on_unresolved=False)) # result : ''

print(varsubst('$UNDEFINED', fail_on_unresolved=False)) # result : ''

print(varsubst('$USER', resolver=DictResolver({'USER': 'tiboun'})))

print(varsubst('{{ USER }}', interpolator=JinjaInterpolator()))
```

# Extras

You may install **varsubst[jinja2]** as well if you intend to interpolate template with Jinja.
If you plan to use jinja2 only, you may install it yourself in your project instead of using this one.