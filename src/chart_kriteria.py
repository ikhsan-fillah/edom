"""Generate bar charts grouped by Periode for each kriteria."""

import re

import plotly.graph_objects as go

from src.utils import get_output_dir, safe_filename, SCORE_MIN, SCORE_MAX


SCORE_COLORS = {
    8: "#4472C4",
    7: "#ED7D31",
    6: "#A5A5A5",
    5: "#FFC000",
    4: "#5B9BD5",
    3: "#70AD47",
    2: "#264478",
    1: "#9E480E",
}

PERIODE_LABELS = {
    "Pra UTS": "Pra UTS Genap 2025/2026",
    "Pra UAS": "Pra UAS Genap 2025/2026",
}


def _score_distribution(series, score_min=SCORE_MIN, score_max=SCORE_MAX):
    """Return counts of each score value from score_min to score_max."""
    counts = series.value_counts().reindex(range(score_min, score_max + 1), fill_value=0)
    return counts


def _kriteria_label(kriteria_col: str) -> str:
    match = re.match(r"\s*(\d+)\.", kriteria_col)
    return f"Kriteria {match.group(1)}" if match else "Kriteria"


def generate_kriteria_chart(df_dosen, kriteria_col: str, nama_dosen: str, save: bool = True):
    """Generate a grouped bar chart for a single kriteria."""
    scores = list(range(SCORE_MAX, SCORE_MIN - 1, -1))

    uts_data = df_dosen[df_dosen["Periode"] == "Pra UTS"][kriteria_col]
    uas_data = df_dosen[df_dosen["Periode"] == "Pra UAS"][kriteria_col]

    uts_counts = _score_distribution(uts_data)
    uas_counts = _score_distribution(uas_data)
    x_labels = [PERIODE_LABELS["Pra UTS"], PERIODE_LABELS["Pra UAS"]]

    fig = go.Figure()
    for score in scores:
        fig.add_bar(
            x=x_labels,
            y=[int(uts_counts[score]), int(uas_counts[score])],
            name=str(score),
            marker_color=SCORE_COLORS[score],
        )

    fig.update_layout(
        title={
            "text": f"[{_kriteria_label(kriteria_col)}] 7-8 sangat baik; 5-6<br>baik; 3-4 cukup; 1-2 kurang",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 30},
        },
        xaxis_title=None,
        yaxis_title=None,
        template="plotly_white",
        barmode="group",
        bargap=0.45,
        bargroupgap=0.05,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font={"size": 18},
        ),
        margin=dict(l=60, r=30, t=105, b=100),
        width=704,
        height=494,
    )
    fig.update_xaxes(tickangle=0, showline=True, linecolor="#DDDDDD", tickfont={"size": 18})
    fig.update_yaxes(gridcolor="#E5E5E5", zerolinecolor="#DDDDDD", tickfont={"size": 16})

    if save:
        out_dir = get_output_dir(nama_dosen)
        match = re.match(r"\s*(\d+)\.", kriteria_col)
        suffix = match.group(1).zfill(2) if match else safe_filename(kriteria_col, 60)
        out_path = out_dir / f"kriteria_{suffix}.png"
        fig.write_image(str(out_path))
        return out_path

    return fig


def generate_all_kriteria_charts(df_dosen, kriteria_list, nama_dosen: str):
    """Generate bar charts for all kriteria columns for a given lecturer."""
    paths = []
    for kriteria_col in kriteria_list:
        path = generate_kriteria_chart(df_dosen, kriteria_col, nama_dosen, save=True)
        paths.append(path)
    return paths
