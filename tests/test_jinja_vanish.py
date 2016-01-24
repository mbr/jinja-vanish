# coding: utf8

from markupsafe import Markup
from jinja_vanish import DynAutoEscapeEnvironment
from six import text_type
import pytest


@pytest.fixture()
def escape_func():
    def begin_end_escape_func(v):
        print('ESCAPING {!r}'.format(v))
        if isinstance(v, Markup):
            return v
        return Markup('BEGIN' + v + 'END')
    return begin_end_escape_func


@pytest.fixture()
def val_a():
    return r'foo\.$<<bar'


@pytest.fixture()
def val_b():
    return u'üä>230-<a>'


@pytest.fixture()
def tpl_src(escape_func, val_a, val_b):
    a, b = val_a, val_b

    tpl = 'hello {{a}} \nworld {{b}}\nsafe {{a|safe}}\n escaped {{b|e}}\n.'

    result = ('hello ' + text_type(escape_func(a)) + ' \nworld ' +
              text_type(escape_func(b)) + '\nsafe ' + a + '\n escaped ' +
              text_type(escape_func(b)) + '\n.')

    return tpl, text_type(result)


@pytest.fixture()
def env(escape_func):
    return DynAutoEscapeEnvironment(autoescape=True, escape_func=escape_func)


@pytest.fixture()
def tpl(env, tpl_src):
    src, _ = tpl_src
    return env.from_string(src)


def test_escaping(tpl, tpl_src, val_a, val_b):
    src, result = tpl_src

    assert tpl.render(a=val_a, b=val_b) == result
