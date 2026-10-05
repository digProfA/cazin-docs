import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cazin Docs", page_icon="🏛️", layout="wide")

st.title("🏛️ Cazin Docs - Pretraga javnih dokumenata")
st.markdown("Nezavisni pretraživač svih odluka, budžeta i javnih poziva Grada Cazina na jednom mjestu.")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data.csv')
        df['kategorija'] = df['kategorija'].fillna('Bez kategorije').astype(str)
        df['godina'] = df['godina'].fillna('Nepoznata').astype(str).str.replace('.0', '', regex=False)
        df['naziv'] = df['naziv'].fillna('Bez naziva').astype(str)
        df['link'] = df['link'].fillna('#').astype(str)
        return df
    except FileNotFoundError:
        st.error("⚠️ Fajl 'data.csv' nije pronađen.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- STATISTIKA (Grafikon) ---
    with st.expander("📊 Pogledaj statistiku dokumenata (Klikni za prikaz)"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Dokumenti po kategorijama:**")
            chart_data = df['kategorija'].value_counts().reset_index()
            chart_data.columns = ['Kategorija', 'Broj dokumenata']
            st.bar_chart(chart_data.set_index('Kategorija'))
        with col2:
            st.markdown("**Dokumenti po godinama:**")
            year_data = df[df['godina'] != 'Nepoznata']['godina'].value_counts().sort_index().reset_index()
            year_data.columns = ['Godina', 'Broj dokumenata']
            st.bar_chart(year_data.set_index('Godina'))
    
    st.divider()

    # --- SIDEBAR FILTERI ---
    st.sidebar.header("🔍 Filteri")
    kategorije = ['Sve'] + sorted(df['kategorija'].unique().tolist())
    selected_kategorija = st.sidebar.selectbox("Kategorija:", kategorije)
    
    godine = ['Sve'] + sorted(df['godina'].unique().tolist(), reverse=True)
    selected_godina = st.sidebar.selectbox("Godina:", godine)
    search_query = st.sidebar.text_input("Pretraga po nazivu:")

    # --- LOGIKA PRETRAGE ---
    filtered_df = df.copy()
    if selected_kategorija != 'Sve': filtered_df = filtered_df[filtered_df['kategorija'] == selected_kategorija]
    if selected_godina != 'Sve': filtered_df = filtered_df[filtered_df['godina'] == selected_godina]
    if search_query: filtered_df = filtered_df[filtered_df['naziv'].str.contains(search_query, case=False, na=False)]

    # --- PRIKAZ REZULTATA ---
    st.write(f"📄 Pronađeno **{len(filtered_df)}** dokumenata.")
    
    for index, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"📁 [{row['naziv']}]({row['link']})")
            st.caption(f"📂 {row['kategorija']} | 📅 {row['godina']}")
            st.divider()

    # --- ZVANIČNI DISCLAIMER ---
    st.markdown("---")
    st.caption(
        "⚠️ **Izjava o odricanju odgovornosti:** Ovo je nezavisna, open-source aplikacija kreirana u edukativne svrhe. "
        "Nismo povezani sa Gradskom upravom Cazina. Svi podaci su preuzeti sa zvaničnog sajta [gradcazin.gov.ba](https://gradcazin.gov.ba) "
        "i linkovi vode direktno ka originalnim dokumentima. Za zvanične informacije posjetite sajt Grada."
    )
