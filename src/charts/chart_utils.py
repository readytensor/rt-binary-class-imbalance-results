from config.chart_cfg import *


def apply_chart_cfg(ax):
    ax.spines["top"].set_visible(border_visible)
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
