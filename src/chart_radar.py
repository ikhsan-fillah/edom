"""Generate radar charts of average scores per kriteria, per Periode."""

import plotly.graph_objects as go

from src.utils import get_output_dir


def _average_scores(df_periode, kriteria_list):
    """Return average score per kriteria for a given periode subset."""
    return [df_periode[col].mean() for col in kriteria_list]


def generate_radar_chart(df_dosen, kriteria_list, periode: str, nama_dosen: str, save: bool = True):
    """Generate a radar chart of average scores for a single Periode ('Pra UTS' or 'Pra UAS')."""
    df_periode = df_dosen[df_dosen["Periode"] == periode]
    avg_scores = _average_scores(df_periode, kriteria_list)

    categories = kriteria_list + [kriteria_list[0]]
    values = avg_scores + [avg_scores[0]]

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                name=periode,
                line=dict(color="#8E44AD"),
            )
        ]
    )
    fig.update_layout(
        title=f"{nama_dosen} — Rata-rata Skor ({periode})",
        polar=dict(radialaxis=dict(visible=True, range=[0, 8])),
        template="plotly_white",
        showlegend=False,
    )

    if save:
        out_dir = get_output_dir(nama_dosen)
        safe_periode = periode.replace(" ", "_")
        out_path = out_dir / f"radar_{safe_periode}.png"
        fig.write_image(str(out_path))
        return out_path

    return fig


def generate_all_radar_charts(df_dosen, kriteria_list, nama_dosen: str):
    """Generate radar charts for both Pra UTS and Pra UAS periods."""
    paths = []
    for periode in ["Pra UTS", "Pra UAS"]:
        path = generate_radar_chart(df_dosen, kriteria_list, periode, nama_dosen, save=True)
        paths.append(path)
    return paths
