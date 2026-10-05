import streamlit as st
import pandas as pd

# Podešavanje izgleda stranice
st.set_page_config(page_title="Cazin Docs", page_icon="🏛️", layout="wide")

st.title("🏛️ Pretraga Dokumenata Grada Cazina")
st.markdown("Pretražite sve odluke, budžete, javne pozive i službene novine na jednom mjestu.")

# Funkcija za učitavanje podataka
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data.csv')
        
        # --- ČIŠĆENJE PODATAKA (Popravka greške) ---
        # Ako nema kategorije, upiši "Bez kategorije"
        df['kategorija'] = df['kategorija'].fillna('Bez kategorije').astype(str)
        
        # Ako nema godine, upiši "Nepoznata"
        df['godina'] = df['godina'].fillna('Nepoznata').astype(str)
        
        # Ponekad Pandas godinu vidi kao 2026.0 (decimalni broj), ovo briše ".0"
        df['godina'] = df['godina'].str.replace('.0', '', regex=False)
        
        # Čistimo i nazive i linkove za svaki slučaj
        df['naziv'] = df['naziv'].fillna('Bez naziva').astype(str)
        df['link'] = df['link'].fillna('#').astype(str)
        # ---------------------------------------------
        
        return df
    except FileNotFoundError:
        st.error("⚠️ Fajl 'data.csv' nije pronađen. Molimo pokrenite 'scraper.py' prvo.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- SIDEBAR (Filteri) ---
    st.sidebar.header("🔍 Filteri")
    
    # Sada je sortiranje sigurno jer nema više NaN (float) vrijednosti
    kategorije = ['Sve'] + sorted(df['kategorija'].unique().tolist())
    selected_kategorija = st.sidebar.selectbox("Kategorija dokumenta:", kategorije)
    
    godine = ['Sve'] + sorted(df['godina'].unique().tolist(), reverse=True)
    selected_godina = st.sidebar.selectbox("Godina:", godine)

    # Polje za pretragu
    search_query = st.text_input("Unesite ključnu riječ (npr. 'budžet', 'plastenici', 'odluka'):")

    # --- LOGIKA PRETRAGE ---
    filtered_df = df.copy()
    
    if selected_kategorija != 'Sve':
        filtered_df = filtered_df[filtered_df['kategorija'] == selected_kategorija]
        
    if selected_godina != 'Sve':
        filtered_df = filtered_df[filtered_df['godina'] == selected_godina]
        
    if search_query:
        # case=False znači da ne razlikuje velika i mala slova
        filtered_df = filtered_df[filtered_df['naziv'].str.contains(search_query, case=False, na=False)]

    # --- PRIKAZ REZULTATA ---
    st.divider()
    st.write(f"📄 Pronađeno **{len(filtered_df)}** dokumenata.")
    
    if len(filtered_df) == 0:
        st.info("Nema rezultata za zadatu pretragu. Pokušajte sa drugom ključnom riječi ili provjerite filtere.")
    else:
        for index, row in filtered_df.iterrows():
            with st.container():
                # Kreiramo klikabilan link
                st.markdown(f"📁 [{row['naziv']}]({row['link']})")
                st.caption(f"📂 Kategorija: `{row['kategorija']}` | 📅 Godina: `{row['godina']}`")
                st.divider()
else:
    st.info("Nema podataka za prikaz. Provjerite da li je `data.csv` u istom folderu kao i `app.py`.")