"""
Streamlit Data App lab.

Run this file with:
    streamlit run 03_streamlit_data_app.py

What to explore:
- Combining data, filters, and layout to build a small dashboard.
- Using multiselects and charts.
- Applying the same pattern to your own CSV or API data.
"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Streamlit Data App", layout="wide")  # Wider layout for tables/charts

st.title("Mini sales dashboard")

data = pd.DataFrame(
    {
        "region": ["North", "South", "West", "East"],
        "sales": [120, 95, 140, 110],
        "rep": ["Alex", "Blake", "Casey", "Dakota"],
    }
)

rep_filter = st.text_input("Filter for rep:", placeholder=list(data["rep"].unique()))

# Wenn der Benutzer einen Namen eingegeben hat, aber dieser ungültig ist, zeige den Fehler
if rep_filter != "" and rep_filter not in data["rep"].values:
    st.error(f"Bitte gib einen gültigen Repräsentanten-Namen ein : ({list(data['rep'].unique())})") 
    # Es ist auch eine gute Praxis, hier st.stop() zu verwenden, um den Rest des Skripts zu stoppen
    st.stop()
       
region_filter = st.multiselect(
    "Regions", options=sorted(data["region"].unique()), default=list(data["region"].unique())
)  # Multiselect drives the filtered view

time_filter = st.time_input("Time frame for data", value="now")

filtered = data.query('region in @region_filter and rep == @rep_filter')
#filtered = data[data["region"].isin(region_filter) & data["rep"] == rep_filter]  # Simple filter using the selection

st.subheader("Table")
st.dataframe(filtered, use_container_width=True)  # Show current slice of data

st.subheader("Chart")

# 1. Definiere die Spalten: Zwei Spalten gleicher Breite (1:1)
col_chart, col_metric = st.columns([1, 1])

# 2. Platziere den Chart in der ersten Spalte (col_chart)
with col_chart:
    st.subheader("Umsatz nach Region")
    
    # st.bar_chart korrekt verwenden
    st.bar_chart(filtered, x="region", y="sales")

# 3. Platziere Metriken in der zweiten Spalte (col_metric)
with col_metric:
    st.subheader("Filter-Kennzahlen")
    
    # Berechne den Gesamtwert aus den gefilterten Daten für st.metric
    total_sales = filtered["sales"].sum()
    
    # Berechne die Anzahl der gefilterten Zeilen
    num_entries = len(filtered)
    
    # st.metric korrekt verwenden
    st.metric("Gesamtumsatz", f"${total_sales}")
    st.metric("Anzahl Regionen", num_entries)


# col_chart = st.bar_chart(filtered, x="region", y="sales")  # Visualize sales per region for the filtered set

# col_metric = st.metric("Data", filtered)
#st.columns(filtered, x="region", y="sales")  # Visualize sales per region for the filtered set

st.markdown(
    """
Next steps:
- Add a search box for reps (`st.text_input`) and filter the table.
- Add date filters if you load time series data.
- Show summary metrics with `st.metric` or `st.columns`.
    """
)
