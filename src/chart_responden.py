"""Generate a line chart showing responder count: Pra UTS vs Pra UAS."""

import plotly.graph_objects as go


def generate_responden_chart(df_dosen, nama_dosen: str):
    """Build a line chart comparing respondent totals per period."""
    counts = df_dosen["Periode"].value_counts().reindex(
        ["Pra UTS", "Pra UAS"],
        fill_value=0,
    )

    fig = go.Figure(
        data=[
            go.Scatter(
                x=counts.index.tolist(),
                y=counts.values.tolist(),
                mode="lines+markers+text",
                text=counts.values.tolist(),
                textposition="top center",
                line={"color": "#27AE60", "width": 3},
                marker={"size": 10},
            )
        ]
    )

    fig.update_layout(
        title=f"{nama_dosen} — Jumlah Responden per Periode",
        xaxis_title="Periode",
        yaxis_title="Jumlah Responden",
        template="plotly_white",
    )

    return fig