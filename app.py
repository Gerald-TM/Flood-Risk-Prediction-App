from Ecolag import lag_df, normalized_df
import streamlit as st
import folium
from streamlit_folium import st_folium

# Load dataframe
df = normalized_df

st.title("ECOLAG: Flood Risk Prediction App")
st.subheader("Make Lagos Safe & Clean")
tab1, tab2, tab3 = st.tabs([
    "📊 LGA Data",
    "⚙️ Normalized Data",
    "🚨 Flood Risk Ranking"
])

with tab1:
    st.dataframe(lag_df.loc[:, :].rename(columns={
        "POPULATION": "Population (people)",
        "LAND AREA": "Land Area (km²)",
        "PER CAPITA WASTE": "Waste per Capita (kg/person/day)",
        "COLLECTION EFFICIENCY": "Collection Efficiency (%)",
        "ANNUAL RAINFALL": "Annual Rainfall (mm/year)"

    }))

with tab2:
    st.dataframe(df[[
        'LGA', 'Population', 'Waste', 'Inefficiency', 'Rainfall']].rename(columns={
        "Population": "Population Density",
        "Waste": "Waste Generation",
        "Inefficiency": "Collection Inefficiency", }).sort_values(by='LGA', ascending=True))

with tab3:
    st.dataframe(df[['LGA', 'Risk', 'Risk_Level']].rename(columns={
        "Risk": "Risk (%)"
    }))
    # st.dataframe(normalized_df)

# st.subheader("Flood Risk Dashboard")

# Show table
# st.dataframe(df[['LGA', 'Risk', 'Risk_Level']])

# Bar chart
st.subheader("Flood Risk Dashboard")
st.bar_chart(df.set_index('LGA')['Risk'])
efficiency_improvement = st.slider(
    "Increase Waste Collection Efficiency (%)",
    0, 50, 0
)

df['Adjusted_Inefficiency'] = df['Inefficiency'] * (1 - efficiency_improvement / 100)

df['Adjusted_Risk'] = (
                              0.35 * df['Waste'] +
                              0.25 * df['Population'] +
                              0.25 * df['Rainfall'] +
                              0.15 * df['Adjusted_Inefficiency']
                      ) * 100

st.bar_chart(df.set_index('LGA')['Adjusted_Risk'])

# Flood Risk Map
# A Map of Lagos showing it's various LGA's and the risk level of flooding by colors
lga_coords = {
    "Agege": [6.6156, 3.3200],
    "Ajeromi-Ifelodun": [6.4550, 3.3400],
    "Alimosho": [6.6090, 3.2950],
    "Amuwo-Odofin": [6.4460, 3.2600],
    "Apapa": [6.4480, 3.3590],
    "Badagry": [6.4150, 2.8830],
    "Epe": [6.5833, 3.9833],
    "Eti-Osa": [6.4333, 3.5000],
    "Ibeju-Lekki": [6.4670, 3.6500],
    "Ifako-Ijaiye": [6.6500, 3.3000],
    "Ikeja": [6.6018, 3.3515],
    "Ikorodu": [6.6194, 3.5100],
    "Kosofe": [6.5800, 3.3800],
    "Lagos Island": [6.4541, 3.3947],
    "Lagos Mainland": [6.5244, 3.3792],
    "Mushin": [6.5270, 3.3500],
    "Ojo": [6.4610, 3.1900],
    "Oshodi-Isolo": [6.5530, 3.3080],
    "Somolu": [6.5400, 3.3800],
    "Surulere": [6.4969, 3.3493]
}


def get_color(risk):
    if risk >= 70:
        return "red"
    elif risk >= 40:
        return "orange"
    else:
        return "green"


m = folium.Map(location=[6.5244, 3.3792], zoom_start=10)

for _, row in normalized_df.iterrows():
    lga = row['LGA']
    risk = row['Risk']

    if lga in lga_coords:
        lat, lon = lga_coords[lga]

        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=get_color(risk),
            fill=True,
            fill_color=get_color(risk),
            fill_opacity=0.7,
            popup=f"{lga}<br>Risk: {risk}"
        ).add_to(m)

st.subheader("Flood Risk Map")
st_folium(m, width=1200, height=600)
