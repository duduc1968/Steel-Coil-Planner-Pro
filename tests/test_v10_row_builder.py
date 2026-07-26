import pandas as pd

from app.core.row_builder import build_complete_rows, classify_cargo

POSITIONS = [
    *(('Bottom', f'B{i}', i, 0) for i in range(1, 7)),
    ('Wedge', 'W1', 7, 1),
    *(('Upper', f'U{i}', i, 2) for i in range(1, 5)),
]


def cargo(n):
    return pd.DataFrame({
        'ID': [f'C{i:03d}' for i in range(n)],
        'Width_m': [1.2 - (i % 3) * 0.02 for i in range(n)],
        'Weight_t': [24 - (i % 5) * 1.5 for i in range(n)],
        'Diameter_m': [1.6 - (i % 2) * 0.05 for i in range(n)],
    })


def test_weight_groups_match_operational_limits():
    df = pd.DataFrame({'Weight_t':[4.9,5,10,15,20,30]})
    out = classify_cargo(df)
    assert out['Size_Group'].tolist() == [
        'Light','Medium','Medium Large','Large','Extra Large','Extra Large'
    ]


def test_builder_creates_only_complete_rows_and_keeps_remainder():
    result = build_complete_rows(cargo(25), POSITIONS)
    assert len(result.rows) == 2
    assert all(len(row) == 11 for row in result.rows)
    assert len(result.remaining) == 3


def test_bwu_roles_are_assigned_by_position_strength():
    result = build_complete_rows(cargo(11), POSITIONS)
    row = result.rows[0]
    bottom = row.iloc[:6]
    wedge = row.iloc[6:7]
    upper = row.iloc[7:]
    assert bottom['Weight_t'].mean() >= upper['Weight_t'].mean()
    assert wedge['Width_m'].iloc[0] <= row['Width_m'].max()


def test_same_group_is_preferred_before_adjacent_group():
    df = pd.DataFrame({
        'ID': [f'L{i}' for i in range(11)] + [f'M{i}' for i in range(11)],
        'Width_m': [1.20] * 22,
        'Weight_t': [18.0] * 11 + [14.0] * 11,
        'Diameter_m': [1.60] * 22,
    })
    result = build_complete_rows(df, POSITIONS)
    assert len(result.rows) == 2
    assert set(result.rows[0]['Size_Group']) == {'Large'}
    assert set(result.rows[1]['Size_Group']) == {'Medium Large'}


def test_adjacent_group_completes_a_row_but_extreme_group_does_not():
    adjacent = pd.DataFrame({
        'ID': [f'XL{i}' for i in range(8)] + [f'L{i}' for i in range(3)],
        'Width_m': [1.2] * 11,
        'Weight_t': [22.0] * 8 + [18.0] * 3,
        'Diameter_m': [1.6] * 11,
    })
    result = build_complete_rows(adjacent, POSITIONS)
    assert len(result.rows) == 1
    assert result.rows[0]['Mixed_Adjacent_Group'].all()

    extreme = pd.DataFrame({
        'ID': [f'XL{i}' for i in range(8)] + [f'LT{i}' for i in range(3)],
        'Width_m': [1.2] * 11,
        'Weight_t': [22.0] * 8 + [4.0] * 3,
        'Diameter_m': [1.6] * 11,
    })
    result = build_complete_rows(extreme, POSITIONS)
    assert len(result.rows) == 0
    assert len(result.remaining) == 11


def test_intelligent_grouping_selects_tight_dimension_cluster():
    # Twelve Large coils are available for an eleven-coil row. One outlier is
    # deliberately much wider/smaller in diameter and should remain outside.
    df = pd.DataFrame({
        'ID': [f'C{i}' for i in range(11)] + ['OUTLIER'],
        'Width_m': [1.20 + (i % 2) * 0.01 for i in range(11)] + [1.80],
        'Weight_t': [18.0 + (i % 3) * 0.1 for i in range(11)] + [18.0],
        'Diameter_m': [1.60 + (i % 2) * 0.01 for i in range(11)] + [1.20],
    })
    result = build_complete_rows(df, POSITIONS)
    assert len(result.rows) == 1
    assert 'OUTLIER' not in set(result.rows[0]['ID'])
    assert result.remaining['ID'].tolist() == ['OUTLIER']
