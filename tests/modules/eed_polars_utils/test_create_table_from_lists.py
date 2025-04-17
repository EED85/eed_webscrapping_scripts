import polars as pl

from eed_webscrapping_scripts.modules import create_table_from_lists


def test_create_table_from_lists():
    """Test the create_table_from_lists function."""
    # Define the input lists and column names

    column_names = ["COL A", "COL B"]
    row_indices = ["1", "2", "3"]
    values = ["l", "l", "m", "h", "m", "h"]
    row_indices_column_name = "index"

    # Create the table using the function
    df = create_table_from_lists(
        column_names=column_names,
        values=values,
        row_indices=row_indices,
        row_indices_column_name=row_indices_column_name,
    )

    # Create thte expected DataFrame manually for comparison

    data = {
        "COL A": ["l", "m", "m"],
        "COL B": ["l", "h", "h"],
        "index": ["1", "2", "3"],
    }
    # Create the DataFrame
    df_expected = pl.DataFrame(data)

    # Check the structure of the created table
    assert df.columns == column_names + [row_indices_column_name]
    assert df.shape == (3, 3)
    assert df.equals(df_expected)
