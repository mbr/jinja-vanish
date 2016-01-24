from functools import wraps

from markupsafe import Markup
from jinja2 import Environment
from jinja2.compiler import CodeGenerator


class LocalOverridingCodeGenerator(CodeGenerator):
    def visit_Template(self, *args, **kwargs):
        super(LocalOverridingCodeGenerator, self).visit_Template(*args,
                                                                 **kwargs)
        overrides = getattr(self.environment, '_codegen_overrides', {})

        if overrides:
            self.writeline('')

        for name, override in overrides.items():
            self.writeline('{} = {}'.format(name, override))


class DynEscapeAutoenvironment(Environment):
    code_generator_class = LocalOverridingCodeGenerator

    def __init__(self, *args, **kwargs):
        escape_func = kwargs.pop('escape_func', None)
        markup_class = kwargs.pop('markup_class', None)

        super(DynEscapeAutoenvironment, self).__init__(*args, **kwargs)

        # we need to disable constant-evaluation at compile time, because it
        # calls jinja's own escape function.
        #
        # this is done by jinja itself if a finalize function is set and it
        # is marked as a contextfunction. this is accomplished by either
        # suppling a no-op contextfunction itself or wrapping an existing
        # finalize in a contextfunction
        if self.finalize:
            if not getattr(self.finalize, 'contextfunction', False):
                _finalize = getattr(self, 'finalize')
                self.finalize = lambda _, v: _finalize(v)
        else:
            self.finalize = lambda _, v: v
        self.finalize.contextfunction = True

        self._codegen_overrides = {}

        if escape_func:
            self._codegen_overrides['escape'] = 'environment.escape_func'
            self.escape_func = escape_func
            self.filters['e'] = escape_func
            self.filters['escape'] = escape_func

        if markup_class:
            self._codegen_overrides['markup'] = 'environment.markup_class'
            self.markup_class = markup_class


def markup_escape_func(f):
    @wraps(f)
    def _(v):
        if isinstance(v, Markup):
            return v
        return Markup(f(v))

    return _
