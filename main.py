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

    /* DataFrame Container */
    [data-testid="stDataFrame"] {
        background-color: #1e293b !important;
    }
    
    /* DataFrame Table */
    [data-testid="stDataFrame"] > div {
        background-color: #1e293b !important;
    }
    
    /* Table Header */
    [data-testid="stDataFrame"] thead tr th {
        background-color: #0f172a !important;
        color: #60a5fa !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #334155 !important;
        padding: 12px !important;
    }
    
    /* Table Body Rows */
    [data-testid="stDataFrame"] tbody tr {
        background-color: #1e293b !important;
        border-bottom: 1px solid #334155 !important;
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background-color: #334155 !important;
    }
    
    /* Table Cells */
    [data-testid="stDataFrame"] tbody tr td {
        color: #e2e8f0 !important;
        padding: 10px !important;
        border-right: 1px solid #334155 !important;
    }
    
    /* Index Column (paling kiri) */
    [data-testid="stDataFrame"] tbody tr th {
        background-color: #0f172a !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        border-right: 2px solid #334155 !important;
    }
    
    /* Data Editor (editable table) */
    [data-testid="stDataEditor"] {
        background-color: #1e293b !important;
    }
    
    [data-testid="stDataEditor"] div[data-testid="stDataFrameResizable"] {
        background-color: #1e293b !important;
    }
    
    /* Data Editor Header */
    [data-testid="stDataEditor"] thead tr th {
        background-color: #0f172a !important;
        color: #60a5fa !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #334155 !important;
    }
    
    /* Data Editor Cells */
    [data-testid="stDataEditor"] tbody tr td {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
    }
    
    [data-testid="stDataEditor"] tbody tr td:hover {
        background-color: #334155 !important;
    }
    
    /* Input dalam Data Editor */
    [data-testid="stDataEditor"] input {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1px solid #3b82f6 !important;
    }
    
    /* Scrollbar untuk tabel */
    [data-testid="stDataFrame"] ::-webkit-scrollbar,
    [data-testid="stDataEditor"] ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    [data-testid="stDataFrame"] ::-webkit-scrollbar-track,
    [data-testid="stDataEditor"] ::-webkit-scrollbar-track {
        background: #0f172a;
        border-radius: 4px;
    }
    
    [data-testid="stDataFrame"] ::-webkit-scrollbar-thumb,
    [data-testid="stDataEditor"] ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    
    [data-testid="stDataFrame"] ::-webkit-scrollbar-thumb:hover,
    [data-testid="stDataEditor"] ::-webkit-scrollbar-thumb:hover {
        background: #3b82f6;
    }
    
    /* Multi-Index Header (untuk kriteria) */
    [data-testid="stDataFrame"] thead tr:first-child th {
        background-color: #1e3a8a !important;
        color: #93c5fd !important;
    }
    
    [data-testid="stDataFrame"] thead tr:last-child th {
        background-color: #0f172a !important;
        color: #60a5fa !important;
    }
    
    /* Column Config Number Input */
    .stNumberInput > div > div > input {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
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

def dict_kriteria_to_multiindex_df(data, posisi="kiri"):
    """Convert kriteria dict to MultiIndex DataFrame"""
    list_M = list(next(iter(data.values())).keys())

    tuples = []

    if posisi == "kiri":
        kolom_labels = list(data.keys())
    elif posisi == "kanan":
        kolom_labels = [f"b{i+1}" for i in range(len(data))]
    else:
        raise ValueError("posisi harus 'kiri' atau 'kanan'")

    for label in kolom_labels:
        tuples.append((label, "derajat keanggotaan"))
        tuples.append((label, "derajat nonkeanggotaan"))

    columns = pd.MultiIndex.from_tuples(tuples, names=["KRITERIA", "NILAI"])
    df = pd.DataFrame(index=list_M, columns=columns)

    for label, (_, nilai_M) in zip(kolom_labels, data.items()):
        for M, nilai in nilai_M.items():
            df.loc[M, (label, "derajat keanggotaan")] = nilai["derajat keanggotaan"]
            df.loc[M, (label, "derajat nonkeanggotaan")] = nilai["derajat nonkeanggotaan"]

    return df


def load_kabupaten_data(uploaded_file, sheet_name):
    """Load kabupaten data from Excel"""
    df_raw = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=None)
    data_dict = {}
    current_kabupaten = None
    collected_rows = []
    
    for idx, row in df_raw.iterrows():
        if isinstance(row[0], str) and row[0].isupper() and row[0] not in ["Kelurahan", "derajat keanggotaan", "derajat nonkeanggotaan"]:
            if current_kabupaten and collected_rows:
                data_dict[current_kabupaten] = pd.DataFrame(
                    collected_rows,
                    columns=["Kelurahan", "derajat keanggotaan", "derajat nonkeanggotaan"]
                )
            current_kabupaten = row[0].strip()
            collected_rows = []
        elif pd.notna(row[0]) and row[0] != "Kelurahan":
            if current_kabupaten:
                collected_rows.append(row.tolist())
    
    if current_kabupaten and collected_rows:
        data_dict[current_kabupaten] = pd.DataFrame(
            collected_rows,
            columns=["Kelurahan", "derajat keanggotaan", "derajat nonkeanggotaan"]
        )
    
    return data_dict

def load_kriteria_data(path, sheet_name):
    """Load kriteria data from Excel"""
    df_kelurahan = pd.read_excel(path, sheet_name="konv kelurahan", header=None)
    match sheet_name:
        case "konv mgtn":
            target_kabupaten = "MAGETAN"
        case "konv bjngr":
            target_kabupaten = "BOJONEGORO"
        case "konv mdiun":
            target_kabupaten = "MADIUN"
    
    
    # target_kabupaten = "KABUPATEN BANDUNG"
    kelurahan_list = []
    current_kabupaten = None

    for idx, row in df_kelurahan.iterrows():
        if (
            isinstance(row[0], str)
            and row[0].isupper()
            and row[0] not in ["Kelurahan", "derajat keanggotaan", "derajat nonkeanggotaan"]
        ):
            current_kabupaten = row[0].strip()

        elif (
            current_kabupaten == target_kabupaten
            and pd.notna(row[0])
            and row[0] != "Kelurahan"
        ):
            kelurahan_list.append(row[0])


    df = pd.read_excel(path, sheet_name=sheet_name, header=None)
    header_row1 = df.iloc[0].ffill()
    header_row2 = df.iloc[1].fillna("")
    
    tuples = list(zip(header_row1, header_row2))
    df.columns = pd.MultiIndex.from_tuples(tuples)
    df = df.iloc[2:].reset_index(drop=True)

    print(kelurahan_list)
    
    result = {}
    for _, row in df.iterrows():
        key = row[("KRITERIA", "")]
        result[key] = {}
        
        for index, M in enumerate(["M1", "M2", "M3", "M4", "M5", "M6"]):
            derajat_keanggotaan = row[(M, "miu")]
            derajat_nonkeanggotaan = row[(M, "v")]
            result[key][kelurahan_list[index]] = {"derajat keanggotaan": float(derajat_keanggotaan), "derajat nonkeanggotaan": float(derajat_nonkeanggotaan)}
    
    return result

def perhitungan_kelurahan(data, kelurahan1, kelurahan2):
    """Calculate kelurahan distance"""
    kolom = {}
    baris = {}
    
    for idx1, row1 in data[kelurahan1.upper()].iterrows():
        list_baris = []
        for idx2, row2 in data[kelurahan2.upper()].iterrows():
            derajat_keanggotaan = abs(row1["derajat keanggotaan"] - row2["derajat keanggotaan"])
            derajat_nonkeanggotaan = abs(row1["derajat nonkeanggotaan"] - row2["derajat nonkeanggotaan"])
            hasil = derajat_keanggotaan + derajat_nonkeanggotaan
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
    gabungan_derajat_keanggotaan = {}
    gabungan_derajat_nonkeanggotaan = {}

    kelurahan = len(dataA['x1'])
    kriteria = len(dataA)

    print("data a :", dataA, "\n\n\n")
    print("data b :", dataB, "\n\n\n")

    list_kelurahan_a = []
    for m in next(iter(dataA.items()))[1]:
        list_kelurahan_a.append(m)
    print(list_kelurahan_a)

    list_kelurahan_b = []
    for m in next(iter(dataB.items()))[1]:
        list_kelurahan_b.append(m)
    print(list_kelurahan_b)
    
    for i, valuesA in dataA.items():
        for j, valuesA_M in valuesA.items():
            for h in range(len(valuesA)):
                derajat_keanggotaan = abs(valuesA_M['derajat keanggotaan'] - dataB[i][list_kelurahan_b[h]]['derajat keanggotaan'])
                derajat_nonkeanggotaan = abs(valuesA_M['derajat nonkeanggotaan'] - dataB[i][list_kelurahan_b[h]]['derajat nonkeanggotaan'])
                key = f'{j}|{list_kelurahan_b[h]}'
                print("key : ", key)
                  
                if key not in gabungan_derajat_keanggotaan:
                    gabungan_derajat_keanggotaan[key] = []
                    gabungan_derajat_nonkeanggotaan[key] = []
                
                gabungan_derajat_keanggotaan[key].append(derajat_keanggotaan)
                gabungan_derajat_nonkeanggotaan[key].append(derajat_nonkeanggotaan)
    baris = {}
    kolom = {}
    
    for i in list_kelurahan_a:
        for j in list_kelurahan_b:
            key = f'{i}|{j}'
            # print(key)
            print(kriteria)
            derajat_keanggotaan_sum = sum(gabungan_derajat_keanggotaan[key])
            derajat_nonkeanggotaan_sum = sum(gabungan_derajat_nonkeanggotaan[key])
            hasil = (1 / kriteria) * (derajat_keanggotaan_sum + derajat_nonkeanggotaan_sum)
            
            if i not in baris:
                baris[i] = []
            if j not in kolom:
                kolom[j] = []
            
            baris[i].append(hasil)
            kolom[j].append(hasil)
    
    min_baris = [min(v) for v in baris.values()]
    min_kolom = [min(v) for v in kolom.values()]
    
    hasil1 = sum(min_baris)
    hasil2 = sum(min_kolom)
    
    return (1 / (4 * kelurahan)) * (hasil1 + hasil2)

def perhitungan_kelurahan_custom(data1, data2):
    """Calculate custom kelurahan distance"""
    baris = {}
    kolom = {}
    
    for a, valuesa in data1.iterrows():
        row_results = []
        for b, valuesb in data2.iterrows():
            hasil = abs(valuesa['derajat keanggotaan Kabupaten 1'] - valuesb["derajat keanggotaan Kabupaten 2"]) + \
                    abs(valuesa["derajat nonkeanggotaan Kabupaten 1"] - valuesb["derajat nonkeanggotaan Kabupaten 2"])
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
    gabungan_derajat_keanggotaan = {}
    gabungan_derajat_nonkeanggotaan = {}

    for i, valuesA in dataA.iterrows():
        for j, valuesA_M in valuesA.items():
            for h in range(len(valuesA)):
                hasil = abs(valuesA_M - dataB.loc[f"b{h+1}", f"{j}"])
                key = f"{j}|{h+1}"

                print("hasil :", f"b{h+1}")
                print("key :", key)
                
                if j == "derajat keanggotaan":
                    if key not in gabungan_derajat_keanggotaan:
                        gabungan_derajat_keanggotaan[key] = []
                    gabungan_derajat_keanggotaan[key].append(hasil)
                else:
                    if key not in gabungan_derajat_nonkeanggotaan:
                        gabungan_derajat_nonkeanggotaan[key] = []
                    gabungan_derajat_nonkeanggotaan[key].append(hasil)
    
    ukuran = int(np.sqrt(len(gabungan_derajat_keanggotaan)))
    baris = {}
    kolom = {}
    
    for i in range(ukuran):
        for j in range(ukuran):
            key = f'M{i+1}|{j+1}'
            derajat_keanggotaan_sum = sum(gabungan_derajat_keanggotaan[key])
            derajat_nonkeanggotaan = sum(gabungan_derajat_nonkeanggotaan[key])
            hasil = (1 / kriteria) * (derajat_keanggotaan_sum + derajat_nonkeanggotaan)
            
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

def render_dark_dataframe(df, show_index=True, index_width="auto"):
    """Render DataFrame sebagai HTML table dengan dark theme"""
    
    # Cek apakah MultiIndex
    is_multiindex = isinstance(df.columns, pd.MultiIndex)
    
    # Auto-detect index width berdasarkan konten
    if index_width == "auto":
        max_len = max(len(str(idx)) for idx in df.index)
        if max_len <= 3:
            index_width = "60px"
        elif max_len <= 10:
            index_width = "100px"
        else:
            index_width = "150px"
    
    html = f"""
    <style>
        .dark-table-container {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(148, 163, 184, 0.1);
            overflow-x: auto;
            margin: 1rem 0;
        }}
        
        .dark-table {{
            width: 100%;
            border-collapse: collapse;
            background-color: #1e293b;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }}
        
        .dark-table thead tr th {{
            background-color: #0f172a;
            color: #60a5fa;
            font-weight: 600;
            padding: 14px 12px;
            text-align: center;
            border: 1px solid #334155;
            font-size: 14px;
        }}
        
        .dark-table thead tr:first-child th {{
            background-color: #1e3a8a;
            color: #93c5fd;
            font-weight: 700;
            font-size: 15px;
        }}
        
        .dark-table tbody tr th {{
            background-color: #0f172a;
            color: #94a3b8;
            font-weight: 600;
            padding: 12px;
            text-align: center;              /* UBAH DARI left KE center */
            border: 1px solid #334155;
            width: {index_width};
            max-width: {index_width};
            min-width: 60px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .dark-table tbody tr td {{
            background-color: #1e293b;
            color: #e2e8f0;
            padding: 12px;
            text-align: center;
            border: 1px solid #334155;
            font-size: 14px;
        }}
        
        .dark-table tbody tr:hover td {{
            background-color: #334155;
            color: #ffffff;
            transition: all 0.2s ease;
        }}
        
        .dark-table tbody tr:hover th {{
            background-color: #1e3a8a;
            color: #93c5fd;
            transition: all 0.2s ease;
        }}
    </style>
    
    <div class="dark-table-container">
        <table class="dark-table">
    """
    
    # === HEADER ===
    html += "<thead>"
    
    if is_multiindex:
        # MultiIndex Header - Level 0
        html += "<tr>"
        if show_index:
            html += '<th rowspan="2"></th>'  # Empty cell for index
        
        for col in df.columns.get_level_values(0).unique():
            # Hitung berapa kolom yang di-span
            span_count = sum(1 for c in df.columns if c[0] == col)
            html += f'<th colspan="{span_count}">{col}</th>'
        html += "</tr>"
        
        # MultiIndex Header - Level 1
        html += "<tr>"
        for col in df.columns:
            html += f'<th>{col[1]}</th>'
        html += "</tr>"
    else:
        # Single Header
        html += "<tr>"
        if show_index:
            html += "<th>Index</th>"
        for col in df.columns:
            html += f"<th>{col}</th>"
        html += "</tr>"
    
    html += "</thead>"
    
    # === BODY ===
    html += "<tbody>"
    
    for idx, row in df.iterrows():
        html += "<tr>"
        
        # Index column
        if show_index:
            html += f"<th>{idx}</th>"
        
        # Data columns
        for val in row:
            # Format number
            if isinstance(val, (int, float)):
                if pd.isna(val):
                    display_val = "-"
                elif isinstance(val, float):
                    display_val = f"{val:.2f}"
                else:
                    display_val = str(val)
            else:
                display_val = str(val)
            
            html += f"<td>{display_val}</td>"
        
        html += "</tr>"
    
    html += "</tbody>"
    html += "</table>"
    html += "</div>"
    
    return html



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
            # Inisialisasi session state untuk selectbox jika belum ada
            if 'kabupaten1' not in st.session_state:
                st.session_state.kabupaten1 = 'MADIUN'
            if 'kabupaten2' not in st.session_state:
                st.session_state.kabupaten2 = 'MADIUN'
            
            # Selectbox di luar tab untuk sinkronisasi
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.kabupaten1 = st.selectbox(
                    "Pilih Kabupaten 1", 
                    ['MADIUN', 'BOJONEGORO', 'MAGETAN'], 
                    key="select_kab1",
                    index=['MADIUN', 'BOJONEGORO', 'MAGETAN'].index(st.session_state.kabupaten1)
                )
            with col2:
                st.session_state.kabupaten2 = st.selectbox(
                    "Pilih Kabupaten 2", 
                    ['MADIUN', 'BOJONEGORO', 'MAGETAN'], 
                    key="select_kab2",
                    index=['MADIUN', 'BOJONEGORO', 'MAGETAN'].index(st.session_state.kabupaten2)
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tab untuk Jenis Data
            tab1, tab2 = st.tabs(["Data Kelurahan", "Data Kriteria"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    data = load_kabupaten_data(uploaded_file, "konv kelurahan")
                    df = data[st.session_state.kabupaten1.upper()].reset_index(drop=True)
                    df.index = df.index + 1
                    df.index.name = "No"
                    st.dataframe(df, use_container_width=True)
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    data = load_kabupaten_data(uploaded_file, "konv kelurahan")
                    df = data[st.session_state.kabupaten2.upper()].reset_index(drop=True)
                    df.index = df.index + 1
                    df.index.name = "No"

                    st.dataframe(df, use_container_width=True)
                
            with tab2:
                konv_map = {
                    'MADIUN': 'konv mdiun',
                    'BOJONEGORO': 'konv bjngr',
                    'MAGETAN': 'konv mgtn'
                }
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    konv_kab1 = konv_map[st.session_state.kabupaten1]
                    data1 = load_kriteria_data(uploaded_file, konv_kab1)
                    data_tampil1 = dict_kriteria_to_multiindex_df(data1)
                    st.dataframe(data_tampil1, use_container_width=True)
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    konv_kab2 = konv_map[st.session_state.kabupaten2]
                    data2 = load_kriteria_data(uploaded_file, konv_kab2)
                    data_tampil2 = dict_kriteria_to_multiindex_df(data2)
                    st.dataframe(data_tampil2, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Hitung dengan Rumus", use_container_width=True):

                st.markdown("<br>", unsafe_allow_html=True)
                

                konv_map = {
                    'MADIUN': 'konv mdiun',
                    'BOJONEGORO': 'konv bjngr',
                    'MAGETAN': 'konv mgtn'
                }
                
                konv_kab1 = konv_map[st.session_state.kabupaten1]
                konv_kab2 = konv_map[st.session_state.kabupaten2]
                
                data = load_kabupaten_data(uploaded_file, "konv kelurahan")
                dataA = load_kriteria_data(uploaded_file, konv_kab1)
                dataB = load_kriteria_data(uploaded_file, konv_kab2)
                
                hasil1 = perhitungan_kelurahan(data, st.session_state.kabupaten1, st.session_state.kabupaten2)
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

    st.markdown("""
    <style>
    /* Mengubah background kotak input */
    div[data-baseweb="input"] > div {
        background-color: #2a2a2a !important;
        border: 1px solid #555 !important;
        border-color : #2a2a2a !important;
    }

    /* Mengubah warna teks label */
    label {
        color: #f0f0f0 !important;
        font-weight: bold;
    }

    /* Mengubah warna teks dalam input */
    input {
        color: white !important;
    }


    .stNumberInput button {
        background-color: #334155 !important;
        color: #2a2a2a !important;
        border: 1px solid #475569 !important;
    }
    
    .stNumberInput button:hover {
        background-color: #3b82f6 !important;
        border-color: #3b82f6 !important;
    }

    .stNumberInput > label {
        color: #2a2a2a !important;
        font-weight: 600 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        kelurahan = st.number_input("Jumlah Kelurahan:", min_value=1, max_value=10, value=3)
    with col2:
        kriteria = st.number_input("Jumlah Kriteria:", min_value=1, max_value=30, value=4)
    
    # Dataset A - Kelurahan
    df_A1 = pd.DataFrame(
        np.zeros((kelurahan, 2)),
        columns=["derajat keanggotaan Kabupaten 1", "derajat nonkeanggotaan Kabupaten 1"],
        index=[f"M{i+1}" for i in range(kelurahan)]
    )

    df_A2 = pd.DataFrame(
        np.zeros((kelurahan, 2)),
        columns=["derajat keanggotaan Kabupaten 2", "derajat nonkeanggotaan Kabupaten 2"],
        index=[f"M{i+1}" for i in range(kelurahan)]
    )
    
    # Dataset B - Kabupaten 1
    kolom_B = []
    for i in range(kelurahan):
        kolom_B.extend([f"derajat keanggotaan M{i+1}", f"derajat nonkeanggotaan M{i+1}"])
    
    df_B = pd.DataFrame(
        np.zeros((kriteria, kelurahan * 2)),
        columns=kolom_B,
        index=[f"x{i+1}" for i in range(kriteria)]
    )
    
    # Dataset C - Kabupaten 2
    df_C = pd.DataFrame(
        np.zeros((kriteria, kelurahan * 2), dtype=float),
        columns=kolom_B,
        index=[f"b{i+1}" for i in range(kriteria)]
    )
    
    column_config = {
        col: st.column_config.NumberColumn(label=col, format="%.2f")
        for col in kolom_B
    }
    
    st.subheader("Data Kelurahan")
    col1, col2 = st.columns(2)
    with col1:
        edited_data_A1 = st.data_editor(
            df_A1,
            key="table_A1",
            use_container_width=True,
            hide_index=False
        )
    with col2:
        edited_data_A2 = st.data_editor(
            df_A2,
            key="table_A2",
            use_container_width=True,
            hide_index=False
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Data Kabupaten 1")
    edited_data_B = st.data_editor(
        df_B,
        key="table_B",
        column_config=column_config,
        use_container_width=True,
        hide_index=False
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Data Kabupaten 2")
    edited_data_C = st.data_editor(
        df_C,
        key="table_C",
        column_config=column_config,
        use_container_width=True,
        hide_index=False
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Hitung dengan Rumus", use_container_width=True):
        hasil1 = perhitungan_kelurahan_custom(edited_data_A1, edited_data_A2)
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