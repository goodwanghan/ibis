from .conftest import BackendTest


def test_where_multiple_conditions(alltypes, alltypes_df):
    expr = alltypes.filter(
        [
            alltypes.float_col > 0,
            alltypes.smallint_col == 9,
            alltypes.int_col < alltypes.float_col * 2,
        ]
    )
    result = expr.execute()

    expected = alltypes_df[
        (alltypes_df['float_col'] > 0)
        & (alltypes_df['smallint_col'] == 9)
        & (alltypes_df['int_col'] < alltypes_df['float_col'] * 2)
    ]

    BackendTest.assert_frame_equal(result, expected)
