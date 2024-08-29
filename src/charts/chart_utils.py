import pandas as pd
import svgwrite
import re

from config import chart_cfg
from config.chart_cfg import *


def apply_chart_cfg(ax):
    ax.spines["top"].set_visible(chart_cfg.border_visible)
    ax.spines["right"].set_visible(border_visible)
    ax.spines["bottom"].set_visible(border_visible)
    ax.spines["left"].set_visible(border_visible)

    ax.set_facecolor("none")

    ax.set_title(
        ax.get_title(),
        color=font_color,
        fontsize=title_font_size,
    )
    ax.set_xlabel(
        ax.get_xlabel(),
        color=font_color,
        fontsize=xlabel_font_size,
    )
    ax.set_ylabel(
        ax.get_ylabel(),
        color=font_color,
        fontsize=ylabel_font_size,
    )

    ax.tick_params(axis="x", colors=font_color, labelsize=tick_font_size)
    ax.tick_params(axis="y", colors=font_color, labelsize=tick_font_size)

    if transparency:
        ax.patch.set_alpha(0)


def find_extreme_cells(df, columns, by="row", extreme="max"):
    """
    Identify the cells to be bolded based on the extreme (max or min) values in specific columns.
    Handles both numeric values and "X +/- Y" format.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        columns (list): List of columns in which to find the extreme values.
        by (str): Whether to bold by 'row' or 'column'. Default is 'row'.
        extreme (str): Whether to bold the 'max' or 'min' values. Default is 'max'.

    Returns:
        dict: A dictionary where the keys are row indices and the values are the column indices
              of the cells to be bolded.
    """
    bold_cells = {}

    def get_x_value(cell_value):
        """Extract the mean (X) value from "X ± Y" format or return the numeric value."""
        if isinstance(cell_value, str) and "±" in cell_value:
            match = re.match(r"([\d.]+)\s*\±\s*([\d.]+)", cell_value)
            if match:
                return float(match.group(1))  # X value (mean)
            else:
                return float("-inf")  # If parsing fails, treat as very low value
        else:
            return (
                float(cell_value)
                if isinstance(cell_value, (int, float))
                else float("-inf")
            )

    if by == "row":
        # Iterate through rows
        for row_idx, row in df.iterrows():
            extreme_value = None
            extreme_cols = []

            for col in columns:
                x_value = get_x_value(row[col])

                # Determine if this is the extreme (max or min) value in the row (for the specified columns)
                if (
                    extreme_value is None
                    or (extreme == "max" and x_value > extreme_value)
                    or (extreme == "min" and x_value < extreme_value)
                ):
                    extreme_value = x_value
                    extreme_cols = [col]  # Reset list with the new extreme value column
                elif x_value == extreme_value:
                    extreme_cols.append(col)  # Handle ties

            # Mark the cells to be bolded in the current row, but only if there is a valid extreme value
            if extreme_cols and extreme_value != float("-inf"):
                bold_cells[row_idx] = extreme_cols

    elif by == "column":
        # Iterate through columns
        for col in columns:
            extreme_value = None
            extreme_rows = []

            for row_idx, cell_value in df[col].iteritems():
                x_value = get_x_value(cell_value)

                # Determine if this is the extreme (max or min) value in the column
                if (
                    extreme_value is None
                    or (extreme == "max" and x_value > extreme_value)
                    or (extreme == "min" and x_value < extreme_value)
                ):
                    extreme_value = x_value
                    extreme_rows = [
                        row_idx
                    ]  # Reset list with the new extreme value row
                elif x_value == extreme_value:
                    extreme_rows.append(row_idx)  # Handle ties

            # Mark the cells to be bolded in the current column, but only if there is a
            # valid extreme value
            if extreme_rows and extreme_value != float("-inf"):
                for row_idx in extreme_rows:
                    if row_idx not in bold_cells:
                        bold_cells[row_idx] = []
                    bold_cells[row_idx].append(col)

    return bold_cells


def df_to_svg(
    df,
    filepath="table.svg",
    bold_first_row=False,
    bold_first_col=False,
    header_font_size=16,
    body_font_size=14,
    header_bg_color="#f0f0f0",
    body_bg_color="#ffffff",
    outer_border_thickness=2,
    inner_border_thickness=1,
    outer_border_color="black",
    inner_border_color="black",
    font_type="Arial",
    highlight_cells=None,
    center_align_columns=None,
    column_widths=None,
    highlight_color=None,
):
    """
    Converts a pandas DataFrame to an SVG with customizable styling, including row
    background colors, highlighted cells, and custom column widths.

    Args:
        df (pd.DataFrame): The DataFrame to be converted to SVG.
        filepath (str): The path where the SVG should be saved.
        bold_first_row (bool): Whether to bold the first row.
        bold_first_col (bool): Whether to bold the first column.
        header_font_size (int): Font size for the first row (header).
        body_font_size (int): Font size for the rest of the table.
        header_bg_color (str): Background color of the first row.
        body_bg_color (str or list): Background color of the rest of the rows.
                            Can be a single color or alternating colors (list).
        outer_border_thickness (int): Thickness of the outer border.
        inner_border_thickness (int): Thickness of the inner borders.
        outer_border_color (str): Color of the outer border.
        inner_border_color (str): Color of the inner borders.
        font_type (str): Font type to be used.
        highlight_cells (dict): A dictionary of row and column indices to be highlighted.
        center_align_columns (list): List of columns to be center-aligned. Default is None.
        column_widths (dict): A dictionary specifying the width of each column
                             (keyed by column name). Default is None (equal widths).
        highlight_color (str): Font color for highlighted cells.
                               Default is None (uses regular font color).

    Returns:
        None
    """
    # Calculate total table width based on column widths
    if column_widths is None:
        # Default equal width for all columns
        column_widths = {col: 200 for col in df.columns}
    else:
        # Ensure that all columns have a specified width; use a default width if not specified
        column_widths = {col: column_widths.get(col, 200) for col in df.columns}

    total_table_width = sum(column_widths.values())
    row_height = 30
    table_height = row_height * (len(df) + 1)  # Including header row

    dwg = svgwrite.Drawing(
        filepath, profile="full", size=(total_table_width, table_height)
    )

    # Ensure center_align_columns is a list even if it's None
    if center_align_columns is None:
        center_align_columns = []

    # Draw the outer table border
    dwg.add(
        dwg.rect(
            insert=(0, 0),
            size=(total_table_width, table_height),
            stroke=outer_border_color,
            fill="none",
            stroke_width=outer_border_thickness,
        )
    )

    # Keep track of column position
    x_position = 0

    # Create table header with customizable styling
    for i, column in enumerate(df.columns):
        col_width = column_widths[column]

        # Background color for the header row
        dwg.add(
            dwg.rect(
                insert=(x_position, 0),
                size=(col_width, row_height),
                stroke=inner_border_color,
                fill=header_bg_color,
                stroke_width=inner_border_thickness,
            )
        )

        # Bold text if specified
        font_weight = "bold" if bold_first_row else "normal"

        # Determine alignment for header
        text_anchor = "middle" if column in center_align_columns else "start"
        text_x_position = (
            x_position + (col_width / 2)
            if column in center_align_columns
            else x_position + 10
        )

        # Add text to header
        dwg.add(
            dwg.text(
                column,
                insert=(text_x_position, row_height - 10),
                font_size=header_font_size,
                font_weight=font_weight,
                font_family=font_type,
                text_anchor=text_anchor,
            )
        )

        # Update x_position for the next column
        x_position += col_width

    # Add the rows with customizable styling
    for row_idx, (_, row) in enumerate(df.iterrows()):
        # Determine background color based on alternating logic
        if isinstance(body_bg_color, list) and len(body_bg_color) == 2:
            bg_color = body_bg_color[row_idx % 2]
        else:
            bg_color = body_bg_color

        x_position = 0  # Reset x_position for each row

        for col_idx, (column_name, cell) in enumerate(row.items()):
            col_width = column_widths[column_name]

            # Background color for body rows
            dwg.add(
                dwg.rect(
                    insert=(x_position, (row_idx + 1) * row_height),
                    size=(col_width, row_height),
                    stroke=inner_border_color,
                    fill=bg_color,
                    stroke_width=inner_border_thickness,
                )
            )

            # Determine if this cell should be highlighted
            is_highlighted = (
                highlight_cells
                and row.name in highlight_cells
                and column_name in highlight_cells[row.name]
            )
            cell_color = highlight_color if is_highlighted else "black"

            # Bold text if specified for first column or based on highlight_cells
            font_weight = (
                "bold"
                if (bold_first_col and col_idx == 0) or is_highlighted
                else "normal"
            )

            # Determine alignment for cells
            text_anchor = "middle" if column_name in center_align_columns else "start"
            text_x_position = (
                x_position + (col_width / 2)
                if column_name in center_align_columns
                else x_position + 10
            )

            # Add text to cell
            dwg.add(
                dwg.text(
                    str(cell),
                    insert=(text_x_position, (row_idx + 2) * row_height - 10),
                    font_size=body_font_size,
                    font_weight=font_weight,
                    font_family=font_type,
                    fill=cell_color,
                    text_anchor=text_anchor,
                )
            )

            # Update x_position for the next column
            x_position += col_width

    # Save the SVG file
    dwg.save()
