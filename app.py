"""EDOM Dashboard - Streamlit app for lecturer evaluation report visualization."""

import streamlit as st

from src.data_loader import load_and_prepare_data, get_dosen_list, filter_by_dosen, get_kriteria_list
from src.chart_kriteria import generate_kriteria_chart
from src.chart_responden import generate_responden_chart
from src.chart_radar import generate_radar_chart
from src.utils import DATA_PATH

st.set_page_config(page_title="EDOM Dashboard", layout="wide")
st.title("Dashboard Rekap EDOM (Evaluasi Dosen oleh Mahasiswa)")


@st.cache_data
def load_data():
    df = load_and_prepare_data(DATA_PATH)
    return df


if not DATA_PATH.exists():
    st.error(f"File data tidak ditemukan: {DATA_PATH}")
    st.stop()

df = load_data()
dosen_list = get_dosen_list(df)
kriteria_list = get_kriteria_list(df)

if not dosen_list:
    st.warning("Data dosen belum tersedia.")
    st.stop()

st.sidebar.header("Filter")
selected_dosen = st.sidebar.selectbox("Pilih Dosen", ["Semua Dosen"] + dosen_list)

st.sidebar.markdown(f"**Total Dosen:** {len(dosen_list)}")
st.sidebar.markdown(f"**Total Responden:** {len(df)}")

dosen_to_display = dosen_list if selected_dosen == "Semua Dosen" else [selected_dosen]

tabs = st.tabs(dosen_to_display)

for tab, nama_dosen in zip(tabs, dosen_to_display):
    with tab:
        df_dosen = filter_by_dosen(df, nama_dosen)
        periode_counts = df_dosen["Periode"].value_counts().reindex(["Pra UTS", "Pra UAS"], fill_value=0)
        st.subheader(nama_dosen)
        st.caption(f"Jumlah responden: {len(df_dosen)}")
        col_uts, col_uas = st.columns(2)
        col_uts.metric("Responden Pra UTS", int(periode_counts["Pra UTS"]))
        col_uas.metric("Responden Pra UAS", int(periode_counts["Pra UAS"]))

        with st.expander("Line Chart - Jumlah Responden", expanded=True):
            fig_responden = generate_responden_chart(df_dosen, nama_dosen, save=False)
            st.plotly_chart(fig_responden, use_container_width=True)
            img_path = generate_responden_chart(df_dosen, nama_dosen, save=True)
            with open(img_path, "rb") as f:
                st.download_button(
                    "Download PNG", f, file_name=img_path.name, mime="image/png",
                    key=f"dl_responden_{nama_dosen}",
                )

        with st.expander("Radar Chart - Rata-rata Skor per Periode"):
            col1, col2 = st.columns(2)
            for col, periode in zip([col1, col2], ["Pra UTS", "Pra UAS"]):
                with col:
                    if periode_counts[periode] == 0:
                        st.warning(f"Tidak ada data {periode} untuk dosen ini.")
                        continue

                    fig_radar = generate_radar_chart(df_dosen, kriteria_list, periode, nama_dosen, save=False)
                    st.plotly_chart(fig_radar, use_container_width=True)
                    img_path = generate_radar_chart(df_dosen, kriteria_list, periode, nama_dosen, save=True)
                    with open(img_path, "rb") as f:
                        st.download_button(
                            f"Download PNG ({periode})", f, file_name=img_path.name, mime="image/png",
                            key=f"dl_radar_{periode}_{nama_dosen}",
                        )

        with st.expander("Bar Chart - Skor per Kriteria (20 chart)"):
            for kriteria_col in kriteria_list:
                fig_bar = generate_kriteria_chart(df_dosen, kriteria_col, nama_dosen, save=False)
                st.plotly_chart(fig_bar, use_container_width=True)
                img_path = generate_kriteria_chart(df_dosen, kriteria_col, nama_dosen, save=True)
                with open(img_path, "rb") as f:
                    st.download_button(
                        "Download PNG", f, file_name=img_path.name, mime="image/png",
                        key=f"dl_bar_{kriteria_col}_{nama_dosen}",
                    )
