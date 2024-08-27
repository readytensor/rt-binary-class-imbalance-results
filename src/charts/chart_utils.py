def apply_chart_cfg(ax):
    ax.spines["top"].set_visible(chart_cfg["border_visible"])
    ax.spines["right"].set_visible(chart_cfg["border_visible"])
    ax.spines["bottom"].set_visible(chart_cfg["border_visible"])
    ax.spines["left"].set_visible(chart_cfg["border_visible"])

    ax.set_facecolor("none")

    ax.set_title(
        ax.get_title(),
        color=chart_cfg["font_color"],
        fontsize=chart_cfg["title_font_size"],
    )
    ax.set_xlabel(
        ax.get_xlabel(),
        color=chart_cfg["font_color"],
        fontsize=chart_cfg["xlabel_font_size"],
    )
    ax.set_ylabel(
        ax.get_ylabel(),
        color=chart_cfg["font_color"],
        fontsize=chart_cfg["ylabel_font_size"],
    )

    ax.tick_params(
        axis="x", colors=chart_cfg["font_color"], labelsize=chart_cfg["tick_font_size"]
    )
    ax.tick_params(
        axis="y", colors=chart_cfg["font_color"], labelsize=chart_cfg["tick_font_size"]
    )

    if chart_cfg["transparency"]:
        ax.patch.set_alpha(0)
