import streamlit as st

# ==========================================
# BAB V: DATABASE MR (Dictionary)
# ==========================================
DATABASE_MR = {
    # ASAM
    "H2SO4": 98.08, "HCL": 36.46, "HNO3": 63.01, "CH3COOH": 60.05, 
    "H3PO4": 98.00, "H2C2O4": 90.03, "HF": 20.01, "HI": 127.91,
    "HBR": 80.91, "HCLO4": 100.46,
    # BASA
    "NAOH": 40.00, "KOH": 56.11, "CA(OH)2": 74.09, "BA(OH)2": 171.34, 
    "NH4OH": 35.05, "MG(OH)2": 58.32, "AL(OH)3": 78.00, "LIOH": 23.95,
    # GARAM
    "NACL": 58.44, "NA2CO3": 105.99, "NAHCO3": 84.01, "KCL": 74.55, 
    "K2SO4": 174.26, "AGNO3": 169.87, "BACL2": 208.23, "CACL2": 110.98, 
    "CUSO4": 159.61, "FESO4": 151.91, "MGSO4": 120.37, "NH4CL": 53.49, 
    "KNO3": 101.10, "NA2S2O3": 158.11, "NA2SO4": 142.04, "K2CO3": 138.21,
    # OKSIDATOR & ORGANIK
    "KMNO4": 158.03, "K2CR2O7": 294.18, "K2CRO4": 194.19, "H2O2": 34.01, 
    "H2O": 18.02, "C2H5OH": 46.07, "CH3OH": 32.04, "C6H12O6": 180.16, 
    "CH4": 16.04, "CHCL3": 119.38, "C6H6": 78.11, "NH3": 17.03, "CO2": 44.01
}
# ==========================================
# BAB VI: FUNGSI KALKULASI (Logic)
# ==========================================
def hitung_mol(massa, mr):
    return massa / mr

def hitung_molaritas(massa, mr, vol_ml):
    return (massa / mr) * (1000 / vol_ml)

def hitung_normalitas(massa, mr, vol_ml, valensi):
    return ((massa / mr) * (1000 / vol_ml)) * valensi

def hitung_ppm(massa_mg, vol_liter):
    return massa_mg / vol_liter

def hitung_persen_bb(massa_zat, massa_total):
    return (massa_zat / massa_total) * 100

def hitung_persen_bv(massa_zat, vol_larutan_ml):
    return (massa_zat / vol_larutan_ml) * 100

def ke_biner(n):
    return bin(int(n)).replace("0b", "")

# ==========================================
# INTERFACE STREAMLIT
# ==========================================
st.set_page_config(page_title="Kalkulator Kimia Industri 2026", layout="wide")
st.title("🧪 Kalkulator Kimia Industri Terpadu")
st.markdown("---")

col_input, col_result = st.columns([1, 1])

with col_input:
    st.subheader("1. Identitas Zat")
    nama = st.text_input("Ketik Rumus Senyawa (Contoh: H2SO4):").upper().strip()
    
    mr_zat = 0.0
    if nama:
        if nama in DATABASE_MR:
            mr_zat = DATABASE_MR[nama]
            st.success(f"Senyawa: {nama} | Mr: {mr_zat}")
        else:
            st.warning("Senyawa tidak ada di database.")
            mr_zat = st.number_input("Masukkan Mr manual:", min_value=0.0)

    st.subheader("2. Parameter Hitung")
    opsi = st.selectbox("Pilih Satuan Yang Dicari:", 
                        ["Mol", "Molaritas (M)", "Normalitas (N)", "PPM (mg/L)", "% B/B", "% B/V"])

    hasil = 0.0
    unit = ""

    # Bab III: Logika Kondisional untuk setiap Rumus
    if mr_zat > 0 or opsi in ["PPM (mg/L)", "% B/B", "% B/V"]:
        if opsi == "Mol":
            gr = st.number_input("Massa (gram):", min_value=0.0, key="mol_gr")
            if st.button("Hitung Mol"):
                hasil = hitung_mol(gr, mr_zat)
                unit = "mol"

        elif opsi == "Molaritas (M)":
            gr = st.number_input("Massa (gram):", min_value=0.0, key="m_gr")
            vol = st.number_input("Volume Larutan (mL):", min_value=0.1, key="m_vol")
            if st.button("Hitung Molaritas"):
                hasil = hitung_molaritas(gr, mr_zat, vol)
                unit = "M"

        elif opsi == "Normalitas (N)":
            gr = st.number_input("Massa (gram):", min_value=0.0, key="n_gr")
            vol = st.number_input("Volume Larutan (mL):", min_value=0.1, key="n_vol")
            val = st.number_input("Valensi (Jumlah n):", min_value=1, step=1)
            if st.button("Hitung Normalitas"):
                hasil = hitung_normalitas(gr, mr_zat, vol, val)
                unit = "N"

        elif opsi == "PPM (mg/L)":
            mg = st.number_input("Massa Zat (mg):", min_value=0.0)
            lit = st.number_input("Volume Pelarut (Liter):", min_value=0.001)
            if st.button("Hitung PPM"):
                hasil = hitung_ppm(mg, lit)
                unit = "ppm"

        elif opsi == "% B/B":
            m_zat = st.number_input("Massa Zat Terlarut (g):", min_value=0.0)
            m_tot = st.number_input("Massa Total Larutan (g):", min_value=0.1)
            if st.button("Hitung % B/B"):
                hasil = hitung_persen_bb(m_zat, m_tot)
                unit = "%"

        elif opsi == "% B/V":
            m_zat = st.number_input("Massa Zat Terlarut (g):", min_value=0.0)
            v_lar = st.number_input("Volume Larutan (mL):", min_value=0.1)
            if st.button("Hitung % B/V"):
                hasil = hitung_persen_bv(m_zat, v_lar)
                unit = "%"

with col_result:
    st.subheader("3. Hasil Analisis")
    if hasil > 0:
        st.metric(label=f"Hasil {opsi}", value=f"{hasil:.4f} {unit}")

    with st.expander("Lihat Database Mr (Bab V)"):
        # Bab IV: Perulangan For
        for k, v in DATABASE_MR.items():
            st.write(f"- {k}: {v}")
