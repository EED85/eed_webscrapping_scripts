import polars as pl


def create_table_from_lists(
    column_names: list,
    values: list,
    row_indices: list = None,
    row_indices_column_name: str = "index",
):
    """
    Creates a table with the given column names, row indices, and values using polars.
    Notice that the values are reshaped into a 2D list based on the number of columns.

    Parameters:
    column_names (list): List of column names.
    row_indices (list): List of row indices.
    values (list): List of values to populate the table.

    Returns:
    pl.DataFrame: The resulting table as a polars DataFrame.
    Example:
        column_names = ["COL A", "COL B"]
        row_indices = ["1", "2", "3"]
        values = ["l", "l", "m", "h", "m", "h"]
        df = create_table(column_names, row_indices, values)

        shape: (3, 2)
        ┌───────┬───────┐
        │ COL A ┆ COL B │
        │ ---   ┆ ---   │
        │ str   ┆ str   │
        ╞═══════╪═══════╡
        │ l     ┆ l     │
        │ m     ┆ h     │
        │ m     ┆ h     │
        └───────┴───────┘

    """
    # Reshape the values list into a 2D list
    reshaped_values = [
        values[i : i + len(column_names)] for i in range(0, len(values), len(column_names))
    ]
    # Create the DataFrame
    df = pl.DataFrame(reshaped_values, schema=column_names)
    # Add the row indices as a new column
    if row_indices is not None:
        df = df.with_columns(pl.Series(row_indices_column_name, row_indices))
    return df
