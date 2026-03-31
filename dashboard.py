import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine




df = pd.read_csv("data.csv")

# Dashboard Title


st.title("Superstore Sales Dashboard")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

annee = st.sidebar.multiselect(
    "Select Year",
    options=df["annee"].unique(),
    default=df["annee"].unique()
)

df_filtered=df[(df["region"].isin(region))
                &(df["category"].isin(category))
                &(df["annee"].isin(annee))]

# Filter


region = st.sidebar.selectbox(
    "Select Region",
    df["region"].unique()
)

df_filtered1 = df[df["region"] == region]


# KPIs


total_sales = df_filtered["sales"].sum()
total_profit = df_filtered["profit"].sum()

profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")


# Sales by Region Chart


sales_region = df_filtered.groupby("region")["sales"].sum().reset_index()

fig, ax = plt.subplots()

sns.barplot(data=sales_region, x="region", y="sales", ax=ax,color="#DEED08")

ax.set_title("Sales by Region")

st.pyplot(fig)



# Calcul des totaux par catégorie
df_cat = df_filtered.groupby("category")[["sales", "profit"]].sum()

# Création du graphique
fig, ax = plt.subplots(figsize=(8,5))

df_cat.plot(
    kind="bar",
    ax=ax,
    color=["#A408ED", "lightgreen"]
)

ax.set_title("Ventes vs Profit par catégorie")
ax.set_xlabel("Catégorie")
ax.set_ylabel("Montant (€)")
ax.set_xticklabels(df_cat.index, rotation=0)
ax.legend(["Ventes", "Profit"])

# Affichage dans Streamlit
st.pyplot(fig)

ventes_categorie=df_filtered.groupby('category')["sales"].sum()
colors = ["#DF1111", "#2905E1", "#0CD520"]

# Création figure
fig, ax = plt.subplots()

# Graphe en secteurs

ventes_categorie.plot(
    kind="pie",
    autopct="%1.1f%%",
    colors=colors,
    startangle=90,
    shadow=True,
    explode=[0.05]*len(ventes_categorie),
    ax=ax
)

ax.set_title("Répartition des ventes par catégorie")
ax.set_ylabel("")  # supprimer label
ax.axis("equal")   # cercle parfait

# Affichage Streamlit
st.pyplot(fig)