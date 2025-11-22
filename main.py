import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image

# ===============================
# 🔧 KONFIGURASI APLIKASI
# ===============================
st.set_page_config(
    page_title="Aplikasi Simulasi Pengukuran Similaritas Kondisi Kekumuhan Wilayah",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Pengukuran similaritas kondisi kekumuhan wilayah kabupaten Madiun, Bojonegoro, Magetan"
    }
)

# Tambahkan CSS untuk hide settings menu
st.markdown("""
<style>
    /* Hide hamburger menu (Settings) */
    #MainMenu {visibility: hidden;}
    
    /* Hide "Made with Streamlit" footer */
    footer {visibility: hidden;}
    
    /* Hide theme switcher button */
    button[kind="header"] {
        display: none !important;
    }
    
    [data-testid="stToolbar"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# 💅 DARK MODE STYLING
# ===============================
st.markdown("""
<style>

    /* FORCE DARK MODE - Override semua tema */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f172a 25%, #1e293b 50%, #0f172a 75%, #0a0e1a 100%) !important;
        background-attachment: fixed !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Paksa warna teks gelap mode */
    .stApp, .stApp * {
        color: #e2e8f0 !important;
    }
    
    /* Override button Streamlit default */
    button[kind="secondary"] {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
    }
    
    /* Hide theme toggle button */
    button[kind="header"] {
        display: none !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f172a 25%, #1e293b 50%, #0f172a 75%, #0a0e1a 100%);
        background-attachment: fixed;
        color: #e2e8f0;
    }
    
    /* Header Card */
    .header-card {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(59, 130, 246, 0.4);
        animation: fadeInDown 0.6s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header-card h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-card p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Custom Card */
    .custom-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(148, 163, 184, 0.1);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(59, 130, 246, 0.3);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .custom-card h2 {
        margin-bottom: 1rem;
        font-size: 1.8rem;
    }
    
    .custom-card p {
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 0;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 56px;
        font-size: 16px;
        font-weight: 600;
        color: white;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border: none;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.6);
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #60a5fa;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Data Editor & DataFrame */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    /* Input Fields */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #1e293b;
        color: #e2e8f0;
        border: 1px solid #334155;
        border-radius: 10px;
        font-weight: 500;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 1px #3b82f6;
    }
    
    /* Slider Container */
    .slider-container {
        position: relative;
        width: 100%;
        height: 500px;
        overflow: hidden;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .slider-wrapper {
        display: flex;
        animation: slide 16s infinite;
        height: 100%;
    }
    
    .slide-image {
        min-width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    @keyframes slide {
        0% { transform: translateX(0); }
        20% { transform: translateX(0); }
        25% { transform: translateX(-100%); }
        45% { transform: translateX(-100%); }
        50% { transform: translateX(-200%); }
        70% { transform: translateX(-200%); }
        75% { transform: translateX(-300%); }
        95% { transform: translateX(-300%); }
        100% { transform: translateX(0); }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Info/Warning/Success Boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        padding: 1rem 1.5rem;
        font-weight: 500;
        background-color: #1e293b;
        color: #e2e8f0;
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        padding: 0;
        border-bottom: 2px solid rgba(51, 65, 85, 0.5);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        border-radius: 12px 12px 0 0;
        font-weight: 600;
        font-size: 16px;
        padding: 0 32px;
        color: #94a3b8;
        background: transparent;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #e2e8f0;
        background: rgba(59, 130, 246, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%);
        color: #60a5fa;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem;
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #334155, transparent);
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# ⚙️ SESSION STATE
# ===============================
if "page" not in st.session_state:
    st.session_state.page = "home"

def goto(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===============================
# 📊 FUNGSI HELPER
# ===============================
def image_to_base64(image_path):
    """Convert image to base64 string"""
    try:
        img = Image.open(image_path)
        target_size = (1200, 800)
        
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS
        
        img = img.resize(target_size, resample)
        buffered = BytesIO()
        img_format = "PNG" if image_path.suffix.lower() == ".png" else "JPEG"
        img.save(buffered, format=img_format, quality=85)
        
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Error loading {image_path.name}: {str(e)}")
        return None

def dict_kriteria_to_multiindex_df(data):
    """Convert kriteria dict to MultiIndex DataFrame"""
    list_M = list(next(iter(data.values())).keys())
    
    tuples = []
    for kriteria in data.keys():
        tuples.append((kriteria, "miu"))
        tuples.append((kriteria, "v"))
    
    columns = pd.MultiIndex.from_tuples(tuples, names=["KRITERIA", "NILAI"])
    df = pd.DataFrame(index=list_M, columns=columns)
    
    for kriteria, nilai_M in data.items():
        for M, nilai in nilai_M.items():
            df.loc[M, (kriteria, "miu")] = nilai["miu"]
            df.loc[M, (kriteria, "v")] = nilai["v"]
    
    return df

def load_kabupaten_data(uploaded_file, sheet_name):
    """Load kabupaten data from Excel"""
    df_raw = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=None)
    data_dict = {}
    current_kabupaten = None
    collected_rows = []
    
    for idx, row in df_raw.iterrows():
        if isinstance(row[0], str) and row[0].isupper() and row[0] not in ["Kelurahan", "miu", "v"]:
            if current_kabupaten and collected_rows:
                data_dict[current_kabupaten] = pd.DataFrame(
                    collected_rows,
                    columns=["Kelurahan", "miu", "v"]
                )
            current_kabupaten = row[0].strip()
            collected_rows = []
        elif pd.notna(row[0]) and row[0] != "Kelurahan":
            if current_kabupaten:
                collected_rows.append(row.tolist())
    
    if current_kabupaten and collected_rows:
        data_dict[current_kabupaten] = pd.DataFrame(
            collected_rows,
            columns=["Kelurahan", "miu", "v"]
        )
    
    return data_dict

def load_kriteria_data(path, sheet_name):
    """Load kriteria data from Excel"""
    df = pd.read_excel(path, sheet_name=sheet_name, header=None)
    header_row1 = df.iloc[0].ffill()
    header_row2 = df.iloc[1].fillna("")
    
    tuples = list(zip(header_row1, header_row2))
    df.columns = pd.MultiIndex.from_tuples(tuples)
    df = df.iloc[2:].reset_index(drop=True)
    
    result = {}
    for _, row in df.iterrows():
        key = row[("KRITERIA", "")]
        result[key] = {}
        
        for M in ["M1", "M2", "M3", "M4", "M5", "M6"]:
            miu = row[(M, "miu")]
            v = row[(M, "v")]
            result[key][M] = {"miu": float(miu), "v": float(v)}
    
    return result

def perhitungan_kelurahan(data, kelurahan1, kelurahan2):
    """Calculate kelurahan distance"""
    kolom = {}
    baris = {}
    
    for idx1, row1 in data[kelurahan1.upper()].iterrows():
        list_baris = []
        for idx2, row2 in data[kelurahan2.upper()].iterrows():
            miu = abs(row1["miu"] - row2["miu"])
            v = abs(row1["v"] - row2["v"])
            hasil = miu + v
            list_baris.append(hasil)
            
            if f'{idx2}' not in kolom:
                kolom[f'{idx2}'] = []
            kolom[f'{idx2}'].append(hasil)
        
        baris[f'{idx1}'] = list_baris
    
    min_a = sum(min(values) for values in baris.values())
    min_b = sum(min(values) for values in kolom.values())
    
    return (1 / 4.6) * (min_a + min_b)

def perhitungan_kriteria(dataA, dataB):
    """Calculate kriteria distance"""
    gabungan_miu = {}
    gabungan_v = {}

    kelurahan = len(dataA['x1'])
    kriteria = len(dataA)
    
    for i, valuesA in dataA.items():
        for j, valuesA_M in valuesA.items():
            for h in range(len(valuesA)):
                miu = abs(valuesA_M['miu'] - dataB[i][f'M{h+1}']['miu'])
                v = abs(valuesA_M['v'] - dataB[i][f'M{h+1}']['v'])
                key = f'{j[1:]}|{h+1}'
                
                if key not in gabungan_miu:
                    gabungan_miu[key] = []
                    gabungan_v[key] = []
                
                gabungan_miu[key].append(miu)
                gabungan_v[key].append(v)
    
    ukuran = int(np.sqrt(len(gabungan_miu)))
    baris = {}
    kolom = {}
    
    for i in range(ukuran):
        for j in range(ukuran):
            key = f'{i+1}|{j+1}'
            miu_sum = sum(gabungan_miu[key])
            v_sum = sum(gabungan_v[key])
            hasil = (1 / kriteria) * (miu_sum + v_sum)
            
            if i+1 not in baris:
                baris[i+1] = []
            if j+1 not in kolom:
                kolom[j+1] = []
            
            baris[i+1].append(hasil)
            kolom[j+1].append(hasil)
    
    min_baris = [min(baris[i+1]) for i in range(ukuran)]
    min_kolom = [min(kolom[j+1]) for j in range(ukuran)]
    
    hasil1 = sum(min_baris)
    hasil2 = sum(min_kolom)
    
    return (1 / (4 * kelurahan)) * (hasil1 + hasil2)

def perhitungan_kelurahan_custom(data):
    """Calculate custom kelurahan distance"""
    baris = {}
    kolom = {}
    
    for a, valuesa in data.iterrows():
        row_results = []
        for b, valuesb in data.iterrows():
            hasil = abs(valuesa['miu Kabupaten 1'] - valuesb["miu Kabupaten 2"]) + \
                    abs(valuesa["v Kabupaten 1"] - valuesb["v Kabupaten 2"])
            row_results.append(hasil)
            
            if b not in kolom:
                kolom[b] = []
            kolom[b].append(hasil)
        
        baris[a] = row_results
    
    min_a = sum(min(values) for values in baris.values())
    min_b = sum(min(values) for values in kolom.values())
    
    return (1 / 4.6) * (min_a + min_b)

def perhitungan_kriteria_custom(dataA, dataB, kelurahan, kriteria):
    """Calculate custom kriteria distance"""
    gabungan_miu = {}
    gabungan_v = {}

    for i, valuesA in dataA.iterrows():
        for j, valuesA_M in valuesA.items():
            for h in range(len(valuesA) // 2):
                hasil = abs(valuesA_M - dataB.loc[i, f"{j.split(' ')[0]} M{h+1}"])
                key = f"{j.split(' ')[1]}|{h+1}"
                
                if j.split(" ")[0] == "miu":
                    if key not in gabungan_miu:
                        gabungan_miu[key] = []
                    gabungan_miu[key].append(hasil)
                else:
                    if key not in gabungan_v:
                        gabungan_v[key] = []
                    gabungan_v[key].append(hasil)
    
    ukuran = int(np.sqrt(len(gabungan_miu)))
    baris = {}
    kolom = {}
    
    for i in range(ukuran):
        for j in range(ukuran):
            key = f'M{i+1}|{j+1}'
            miu_sum = sum(gabungan_miu[key])
            v_sum = sum(gabungan_v[key])
            hasil = (1 / kriteria) * (miu_sum + v_sum)
            
            if i+1 not in baris:
                baris[i+1] = []
            if j+1 not in kolom:
                kolom[j+1] = []
            
            baris[i+1].append(hasil)
            kolom[j+1].append(hasil)
    
    min_baris = [min(baris[i+1]) for i in range(ukuran)]
    min_kolom = [min(kolom[j+1]) for j in range(ukuran)]
    
    hasil1 = sum(min_baris)
    hasil2 = sum(min_kolom)
    
    return (1 / (4 * kelurahan)) * (hasil1 + hasil2)

# ===============================
# 🏠 HALAMAN HOME
# ===============================
if st.session_state.page == "home":
    st.markdown("""
        <div class="header-card">
            <h1>Aplikasi Simulasi Pengukuran Similaritas<br>Kondisi Kekumuhan Wilayah</h1>
            <p>Pengukuran similaritas kondisi kekumuhan wilayah kabupaten Madiun, Bojonegoro, Magetan</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 2], gap="large")
    
    with col_left:
        current_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
        
        possible_paths = [
            [current_dir / "images" / "home 1.jpg", current_dir / "images" / "home 2.jpg",
             current_dir / "images" / "home 3.jpg", current_dir / "images" / "home 4.jpg"],
            [Path("images/home 1.jpg"), Path("images/home 2.jpg"),
             Path("images/home 3.jpg"), Path("images/home 4.jpg")],
            [Path("home 1.jpg"), Path("home 2.jpg"), Path("home 3.jpg"), Path("home 4.jpg")]
        ]
        
        image_paths = None
        for paths in possible_paths:
            if all(p.exists() for p in paths):
                image_paths = paths
                break
        
        if image_paths:
            img_base64_list = [image_to_base64(path) for path in image_paths]
            img_base64_list = [img for img in img_base64_list if img is not None]
            
            if img_base64_list:
                slider_html = '<div class="slider-container"><div class="slider-wrapper">'
                for i, img_base64 in enumerate(img_base64_list):
                    slider_html += f'<img src="data:image/jpeg;base64,{img_base64}" class="slide-image" alt="Slide {i+1}">'
                slider_html += '</div></div>'
                st.markdown(slider_html, unsafe_allow_html=True)
            else:
                st.error("❌ Gagal memuat gambar. Periksa format file.")
        else:
            st.markdown("""
                <div class="slider-container">
                    <div style="display: flex; align-items: center; justify-content: center; height: 100%; padding: 2rem; text-align: center;">
                        <div>
                            <h3 style="color: #60a5fa; margin-bottom: 1rem;">Gambar Belum Tersedia</h3>
                            <p style="color: #94a3b8; font-size: 1rem; line-height: 1.6;">
                                Silakan letakkan gambar Anda di folder:<br>
                                <code style="background: #1e293b; padding: 0.5rem 1rem; border-radius: 8px; display: inline-block; margin-top: 0.5rem;">
                                    images/home 1.jpg<br>
                                    images/home 2.jpg<br>
                                    images/home 3.jpg<br>
                                    images/home 4.jpg
                                </code>
                            </p>
                            <p style="color: #64748b; font-size: 0.9rem; margin-top: 1rem;">
                                Format yang didukung: .jpg, .jpeg, .png
                            </p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class="custom-card" style="margin-bottom: 0;">
                <h2 style="color: #60a5fa;">Data Excel</h2>
                <p>Gunakan data yang telah disiapkan untuk melakukan simulasi yang interaktif.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Data Excel", key="btn_excel"):
            goto("excel")
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class="custom-card" style="margin-bottom: 0;">
                <h2 style="color: #34d399;">Data Custom</h2>
                <p>Menginput data sesuai dengan kebutuhan untuk simulasi yang interaktif.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Data Custom", key="btn_custom"):
            goto("custom")

# ===============================
# 📘 HALAMAN EXCEL
# ===============================
elif st.session_state.page == "excel":
    st.markdown("""
    <div class="header-card">
        <h1>Excel Data Analysis</h1>
        <p>Analisis data dari Excel</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_back, col_space = st.columns([1, 5])
    with col_back:
        if st.button("Kembali", key="back_excel"):
            goto("home")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    default_folder = "data"
    uploaded_file = Path(default_folder) / 'data pembuatan aplikasi.xlsx'
    
    if uploaded_file.exists():
        try:
            # Tab untuk Jenis Data
            tab1, tab2 = st.tabs(["Data Kelurahan", "Data Kriteria"])
            
            with tab1:
                st.markdown("### Pilih Kabupaten")
                kabupaten = st.radio(
                    "kabupaten_kelurahan",
                    ["Madiun", "Bojonegoro", "Magetan"],
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                data = load_kabupaten_data(uploaded_file, "konv kelurahan")
                st.dataframe(data[kabupaten.upper()], use_container_width=True)
            
            with tab2:
                st.markdown("### Pilih Kabupaten")
                kabupaten = st.radio(
                    "kabupaten_kriteria",
                    ["Madiun", "Bojonegoro", "Magetan"],
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                konv_map = {
                    'Madiun': 'konv mdiun',
                    'Bojonegoro': 'konv bjngr',
                    'Magetan': 'konv mgtn'
                }
                konv_kab = konv_map[kabupaten]
                data = load_kriteria_data(uploaded_file, konv_kab)
                data_tampil = dict_kriteria_to_multiindex_df(data)
                st.dataframe(data_tampil, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                kabupaten1 = st.selectbox("Pilih Kabupaten 1", ['MADIUN', 'BOJONEGORO', 'MAGETAN'])
            with col2:
                kabupaten2 = st.selectbox("Pilih Kabupaten 2", ['MADIUN', 'BOJONEGORO', 'MAGETAN'])
            
            if st.button("Hitung dengan Rumus", use_container_width=True):
                konv_map = {
                    'MADIUN': 'konv mdiun',
                    'BOJONEGORO': 'konv bjngr',
                    'MAGETAN': 'konv mgtn'
                }
                
                konv_kab1 = konv_map[kabupaten1]
                konv_kab2 = konv_map[kabupaten2]
                
                data = load_kabupaten_data(uploaded_file, "konv kelurahan")
                dataA = load_kriteria_data(uploaded_file, konv_kab1)
                dataB = load_kriteria_data(uploaded_file, konv_kab2)
                
                hasil1 = perhitungan_kelurahan(data, kabupaten1, kabupaten2)
                hasil2 = perhitungan_kriteria(dataA, dataB)
                hasil3 = (1 / 2) * (hasil1 + hasil2)
                hasil4 = 1 - hasil3
                
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                        padding: 3rem 2rem;
                        border-radius: 20px;
                        text-align: center;
                        box-shadow: 0 20px 60px rgba(59, 130, 246, 0.5);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        animation: fadeInUp 0.6s ease-out;
                    ">
                        <div style="
                            font-size: 0.9rem;
                            font-weight: 600;
                            color: rgba(255, 255, 255, 0.9);
                            text-transform: uppercase;
                            letter-spacing: 2px;
                            margin-bottom: 1rem;
                        ">
                            Nilai Kemiripan
                        </div>
                        <div style="
                            font-size: 4rem;
                            font-weight: 700;
                            color: white;
                            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                            margin-bottom: 0.5rem;
                        ">
                            {hasil4:.4f}
                        </div>
                        <div style="
                            font-size: 1rem;
                            color: rgba(255, 255, 255, 0.85);
                            font-weight: 400;
                        ">
                            Tingkat similaritas kondisi kekumuhan wilayah
                        </div>
                    </div>
                    
                    <style>
                        @keyframes fadeInUp {{
                            from {{
                                opacity: 0;
                                transform: translateY(30px);
                            }}
                            to {{
                                opacity: 1;
                                transform: translateY(0);
                            }}
                        }}
                    </style>
                """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Pastikan file Excel valid.")
    else:
        st.info("Pastikan file Excel telah disiapkan di folder 'data/data pembuatan aplikasi.xlsx'")

# ===============================
# ✨ HALAMAN CUSTOM
# ===============================
elif st.session_state.page == "custom":
    st.markdown("""
    <div class="header-card">
        <h1>Custom Data Creator</h1>
        <p>Buat dan analisis data custom Anda sendiri</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_back, col_space = st.columns([1, 5])
    with col_back:
        if st.button("Kembali", key="back_custom"):
            goto("home")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="custom-card">
            <h3 style="color: #60a5fa;">Input Data Sesuai Kebutuhan</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        kelurahan = st.number_input("Jumlah Kelurahan:", min_value=1, max_value=10, value=3)
    with col2:
        kriteria = st.number_input("Jumlah Kriteria:", min_value=1, max_value=30, value=4)
    
    # Dataset A - Kelurahan
    df_A = pd.DataFrame(
        np.zeros((kelurahan, 4)),
        columns=["miu Kabupaten 1", "v Kabupaten 1", "miu Kabupaten 2", "v Kabupaten 2"],
        index=[f"M{i+1}" for i in range(kelurahan)]
    )
    
    # Dataset B - Kabupaten 1
    kolom_B = []
    for i in range(kelurahan):
        kolom_B.extend([f"miu M{i+1}", f"v M{i+1}"])
    
    df_B = pd.DataFrame(
        np.zeros((kriteria, kelurahan * 2)),
        columns=kolom_B,
        index=[f"X{i+1}" for i in range(kriteria)]
    )
    
    # Dataset C - Kabupaten 2
    df_C = pd.DataFrame(
        np.zeros((kriteria, kelurahan * 2), dtype=float),
        columns=kolom_B,
        index=[f"X{i+1}" for i in range(kriteria)]
    )
    
    column_config = {
        col: st.column_config.NumberColumn(label=col, format="%.2f")
        for col in kolom_B
    }
    
    st.subheader("Data Kelurahan")
    edited_data_A = st.data_editor(
        df_A,
        key="table_A",
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Data Kabupaten 1")
    edited_data_B = st.data_editor(
        df_B,
        key="table_B",
        column_config=column_config,
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Data Kabupaten 2")
    edited_data_C = st.data_editor(
        df_C,
        key="table_C",
        column_config=column_config,
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Hitung dengan Rumus", use_container_width=True):
        hasil1 = perhitungan_kelurahan_custom(edited_data_A)
        hasil2 = perhitungan_kriteria_custom(edited_data_B, edited_data_C, kelurahan, kriteria)
        hasil3 = (1 / 2) * (hasil1 + hasil2)
        hasil4 = 1 - hasil3
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Modern Result Card
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                padding: 3rem 2rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(59, 130, 246, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.2);
                animation: fadeInUp 0.6s ease-out;
            ">
                <div style="
                    font-size: 0.9rem;
                    font-weight: 600;
                    color: rgba(255, 255, 255, 0.9);
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    margin-bottom: 1rem;
                ">
                    Nilai Kemiripan
                </div>
                <div style="
                    font-size: 4rem;
                    font-weight: 700;
                    color: white;
                    text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                    margin-bottom: 0.5rem;
                ">
                    {hasil4:.4f}
                </div>
                <div style="
                    font-size: 1rem;
                    color: rgba(255, 255, 255, 0.85);
                    font-weight: 400;
                ">
                    Tingkat similaritas kondisi kekumuhan wilayah
                </div>
            </div>
            
            <style>
                @keyframes fadeInUp {{
                    from {{
                        opacity: 0;
                        transform: translateY(30px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
            </style>
        """, unsafe_allow_html=True)