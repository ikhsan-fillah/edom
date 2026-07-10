"""Generate a line chart showing responder count trend: Pra UTS vs Pra UAS."""

import plotly.graph_objects as go

from src.utils import get_output_dir


def generate_responden_chart(df_dosen, nama_dosen: str, save: bool = True):
    """Generate a line chart comparing number of responders per Periode."""
    counts = df_dosen["Periode"].value_counts().reindex(["Pra UTS", "Pra UAS"], fill_value=0)

    fig = go.Figure(
        data=[
            go.Scatter(
                x=counts.index.tolist(),
                y=counts.values.tolist(),
                mode="lines+markers+text",
                text=counts.values.tolist(),
                textposition="top center",
                line=dict(color="#27AE60", width=3),
                marker=dict(size=10),
            )
        ]
    )
    fig.update_layout(
        title=f"{nama_dosen} — Jumlah Responden per Periode",
        xaxis_title="Periode",
        yaxis_title="Jumlah Responden",
        template="plotly_white",
    )

    if save:
        out_dir = get_output_dir(nama_dosen)
        out_path = out_dir / "line_responden.png"
        fig.write_image(str(out_path))
        return out_path

    return fig
