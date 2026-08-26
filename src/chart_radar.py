"""Generate radar charts of average scores per kriteria, per Periode."""

import plotly.graph_objects as go


def _average_scores(df_periode, kriteria_list):
    """Return mean score for every kriteria in one period."""
    return [df_periode[col].mean() for col in kriteria_list]


def generate_radar_chart(df_dosen, kriteria_list, periode: str, nama_dosen: str):
    """Build a radar chart for one lecturer and one period."""
    df_periode = df_dosen[df_dosen["Periode"] == periode]
    avg_scores = _average_scores(df_periode, kriteria_list)

    categories = list(kriteria_list)
    categories.append(kriteria_list[0])

    values = list(avg_scores)
    values.append(avg_scores[0])

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                name=periode,
                line={"color": "#8E44AD"},
            )
        ]
    )

    fig.update_layout(
        title=f"{nama_dosen} — Rata-rata Skor ({periode})",
        polar={
            "radialaxis": {
                "visible": True,
                "range": [0, 8],
            }
        },
        template="plotly_white",
        showlegend=False,
    )

    return fig