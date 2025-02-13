import os
import uuid

import numpy as np
import pandas.testing as tm
import pytest

import ibis
import ibis.config as config
import ibis.expr.types as ir
from ibis.backends.sqlite import Backend
from ibis.util import guid


def test_file_not_exist_and_create():
    path = f'__ibis_tmp_{guid()}.db'

    with pytest.raises(FileNotFoundError):
        ibis.sqlite.connect(path)

    con = ibis.sqlite.connect(path, create=True)
    try:
        assert os.path.exists(path)
    finally:
        con.con.dispose()
        os.remove(path)


def test_table(con):
    table = con.table('functional_alltypes')
    assert isinstance(table, ir.TableExpr)


def test_column_execute(alltypes, df):
    expr = alltypes.double_col
    result = expr.execute()
    expected = df.double_col
    tm.assert_series_equal(result, expected)


def test_literal_execute(con):
    expr = ibis.literal('1234')
    result = con.execute(expr)
    assert result == '1234'


def test_simple_aggregate_execute(alltypes, df):
    expr = alltypes.double_col.sum()
    result = expr.execute()
    expected = df.double_col.sum()
    np.testing.assert_allclose(result, expected)


def test_list_tables(con):
    assert con.list_tables()
    assert len(con.list_tables(like='functional')) == 1


def test_attach_file(dbpath):
    client = Backend().connect(None)

    client.attach('foo', dbpath)
    client.attach('bar', dbpath)

    foo_tables = client.list_tables(database='foo')
    bar_tables = client.list_tables(database='bar')

    assert foo_tables == bar_tables


def test_compile_toplevel():
    t = ibis.table([('foo', 'double')], name='t0')

    # it works!
    expr = t.foo.sum()
    result = ibis.sqlite.compile(expr)
    expected = """\
SELECT sum(t0.foo) AS sum 
FROM t0 AS t0"""  # noqa
    assert str(result) == expected


def test_create_and_drop_table(con):
    t = con.table('functional_alltypes')
    name = str(uuid.uuid4())
    con.create_table(name, t.limit(5))
    new_table = con.table(name)
    tm.assert_frame_equal(new_table.execute(), t.limit(5).execute())
    con.drop_table(name)
    assert name not in con.list_tables()


def test_verbose_log_queries(con):
    queries = []

    with config.option_context('verbose', True):
        with config.option_context('verbose_log', queries.append):
            con.table('functional_alltypes')['year'].execute()

    assert len(queries) == 1
    (query,) = queries
    expected = 'SELECT t0.year \n'
    expected += 'FROM base.functional_alltypes AS t0\n'
    expected += ' LIMIT ? OFFSET ?'
    assert query == expected


def test_table_equality(dbpath):
    con1 = ibis.sqlite.connect(dbpath)
    batting1 = con1.table("batting")

    con2 = ibis.sqlite.connect(dbpath)
    batting2 = con2.table("batting")

    assert batting1.op() == batting2.op()
    assert batting1.equals(batting2)


def test_table_inequality(dbpath):
    con = ibis.sqlite.connect(dbpath)

    batting = con.table("batting")
    functional_alltypes = con.table("functional_alltypes")

    assert batting.op() != functional_alltypes.op()
    assert not batting.equals(functional_alltypes)
