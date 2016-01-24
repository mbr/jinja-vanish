Jinja vanish: Escape like a ninja
=================================

When using `Jinja2`_-templates to output non-HTML contents, autoescaping cannot
be used because it is hardcoded to work with an HTML ``escape`` function and
`MarkupSafe`_'s Markup objects.

`jinja_vanish` enables implementing custom auto-escapes by overriding the
``escape`` function inside the generated template code using an extended
code-generator and replacing the built-in filters ``|e`` and ``|escape``. Usage
is fairly simple, here is an example that uses `psycopg2`'s ``mogrify()``
function to escape SQL for Postgres:

.. code-block:: python

    from datetime import datetime

    from jinja_vanish import DynAutoEscapeEnvironment, markup_escape_func
    from psycopg2.extensions import adapt

    @markup_escape_func
    def sql_escape(v):
        # the decorator handles wrapping/unwrapping in Markup(), but is
        # otherwise not necessary
        return adapt(v)


    env = DynAutoEscapeEnvironment(autoescape=True, escape_func=sql_escape)
    tpl = env.from_string('SELECT * FROM foo where post_date <= {{now}}')

    print(tpl.render(now=datetime.now()))

Running it outputs::

    SELECT * FROM foo where post_date <= '2016-01-24T23:23:22.727789'::timestamp



.. _Jinja2: http://jinja.pocoo.org
.. _MarkupSafe: https://pypi.python.org/pypi/MarkupSafe
