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
