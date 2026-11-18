import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Dashboard Prakiraan Cuaca & Iklim", layout="wide")

# Fungsi untuk mengambil teks & gambar langsung dari halaman Dinamika Atmosfer BMKG
@st.cache_data(ttl=3600)
def ambil_info_iod_enso():
    url = "https://www.bmkg.go.id/iklim/dinamika-atmosfer"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")
    
    paragraf = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 60]
    gambar = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and ("iklim" in src or "dinamika" in src or "enso" in src or "iod" in src or "upload" in src or "cdn" in src):
            if src.startswith("/"):
                src = "https://www.bmkg.go.id" + src
            if src.startswith("http") and src not in gambar:
                gambar.append(src)
    return paragraf, gambar

# --- MENU NAVIGASI DI SIDEBAR ---
st.sidebar.title("🧭 Menu Dashboard")
menu_pilihan = st.sidebar.radio(
    "Pilih Tampilan Data:",
    ["Beranda", "Pertumbuhan Awan", "IOD dan ENSO", "RASON"]
)

# --- HALAMAN 1: BERANDA ---
if menu_pilihan == "Beranda":
    st.title("🌦️ Selamat Datang di Dashboard Prakiraan")
    st.write("Silakan pilih menu di panel sebelah kiri untuk menampilkan informasi dari BMKG:")
    st.markdown(
        "- **Pertumbuhan Awan:** Peta prakiraan potensi pertumbuhan awan hujan.\n"
        "- **IOD dan ENSO:** Informasi dinamika atmosfer (Indian Ocean Dipole & El Nino-Southern Oscillation).\n"
        "- **RASON:** Peta pengamatan udara atas / Radiosonde (BMKG Aviation)."
    )
    st.info("👈 Pilih menu di sebelah kiri untuk memulai.")

# --- HALAMAN 2: PERTUMBUHAN AWAN ---
elif menu_pilihan == "Pertumbuhan Awan":
    st.title("☁️ Prakiraan Potensi Pertumbuhan Awan Hujan")
    st.caption("Sumber: BMKG Signature")
    
    url_awan = "https://signature.bmkg.go.id/aware/dashboard-met/#/id/prakiraan/potensi-pertumbuhan-awan-hujan"
    st.link_button("↗️ Buka Peta Layar Penuh di Tab Baru", url_awan)
    components.iframe(url_awan, height=780, scrolling=True)

# --- HALAMAN 3: IOD DAN ENSO ---
elif menu_pilihan == "IOD dan ENSO":
    st.title("🌊 Dinamika Atmosfer: IOD dan ENSO")
    url_dinamika = "https://www.bmkg.go.id/iklim/dinamika-atmosfer"
    
    col_ket, col_btn = st.columns([3, 1])
    col_ket.caption("Data diambil langsung dari portal Iklim BMKG")
    col_btn.link_button("🌐 Buka Halaman Asli BMKG", url_dinamika)
    st.markdown("---")
    
    try:
        with st.spinner("Mengambil data terbaru dari BMKG..."):
            teks_list, img_list = ambil_info_iod_enso()
            
        if img_list:
            st.subheader("📊 Peta & Grafik Analisis Terbaru")
            for img_url in img_list[:4]:
                st.image(img_url, use_container_width=True)
                
        if teks_list:
            st.subheader("📝 Ringkasan Analisis Dinamika Atmosfer")
            for teks in teks_list[:8]:
                st.write(teks)
        else:
            st.warning("Konten halaman dimuat secara dinamis oleh server BMKG. Silakan klik tombol 'Buka Halaman Asli BMKG' di pojok kanan atas untuk melihat grafik lengkapnya.")
            
    except Exception as e:
        st.error(f"Gagal terhubung ke server BMKG: {e}")

# --- HALAMAN 4: RASON ---
elif menu_pilihan == "RASON":
    st.title("🎈 Pengamatan Udara Atas (RASON)")
    st.caption("Sumber: BMKG Aviation Maps")
    st.markdown("---")
    
    url_rason = "https://web-aviation.bmkg.go.id/maps"
    st.info("Portal BMKG Aviation membatasi tampilan peta langsung di dalam frame dashboard eksternal demi keamanan sistem. Klik tombol di bawah untuk membuka peta interaktif RASON secara penuh:")
    st.link_button("🗺️ Buka Peta Interaktif RASON (BMKG Aviation)", url_rason, type="primary")