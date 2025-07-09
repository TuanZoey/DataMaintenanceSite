import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    drivers = pd.read_csv("F1_Driver/drivers.csv")
    results = pd.read_csv("F1_Driver/results.csv")
    races = pd.read_csv("F1_Driver/races.csv")
    df = results.merge(drivers, on="driverId").merge(races, on="raceId")
    return df, drivers

df, drivers = load_data()
driver_names = sorted(df["surname"].unique())

# Create tabs
tab1, tab2, tab3 = st.tabs(["🏁 Career Trends Overview", "👤 Driver Dashboard", "⚔️ Driver Comparison"])


# -----------------------------------
# Tab 1: Career Trends Overview
# -----------------------------------
with tab1:
    st.title("🏁 Formula 1: Career Trends Overview")
    st.markdown("Explore the overall performance trends of Formula 1 drivers with advanced visualizations.")

    graph_type = st.selectbox("Choose Visualization", ["Violin Plot", "Swarm Plot", "Boxplot", "Scatter"])
    
    if graph_type == "Violin Plot":
        st.subheader("🎻 Violin Plot: Points by Nationality")
        fig, ax = plt.subplots(figsize=(14, 6))
        sns.violinplot(data=df[df["points"] > 0], x="nationality", y="points", scale="width", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif graph_type == "Swarm Plot":
        st.subheader("🐝 Swarm Plot: Points per Race by Constructor")
        fig, ax = plt.subplots(figsize=(14, 6))
        sns.swarmplot(data=df[df["points"] > 0], x="constructorId", y="points", hue="nationality", dodge=True, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif graph_type == "Boxplot":
        st.subheader("📦 Boxplot: Points per Year")
        fig, ax = plt.subplots(figsize=(14, 6))
        sns.boxplot(data=df[df["points"] > 0], x="year", y="points", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif graph_type == "Scatter":
        st.subheader("🎯 Scatter: Grid vs Final Position")
        scatter_df = df[(df["positionOrder"] < 20) & (df["grid"] < 20)]
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.scatterplot(data=scatter_df, x="grid", y="positionOrder", hue="surname", alpha=0.7, ax=ax)
        ax.set_xlabel("Grid Position")
        ax.set_ylabel("Final Position")
        st.pyplot(fig)

# -----------------------------------
# Tab 2: Personal Driver Dashboard
# -----------------------------------
with tab2:
    st.title("👤 Personal Driver Dashboard")

    selected_driver = st.selectbox("Select a Driver", driver_names)
    driver_data = df[df["surname"] == selected_driver]
    driver_profile = driver_data.iloc[0]

    # Driver image
    image_path = Path(f"driver_images/{selected_driver.lower()}.png")
    if image_path.exists():
        st.image(str(image_path), caption=selected_driver, width=200)

    st.markdown(f"**Full Name:** {driver_profile['forename']} {driver_profile['surname']}")
    st.markdown(f"**DOB:** {driver_profile['dob']}")
    st.markdown(f"**Nationality:** {driver_profile['nationality']}")

    # Line chart of points by season
    points_season = driver_data.groupby("year")["points"].sum().reset_index()
    st.subheader("📊 Points by Season")
    fig, ax = plt.subplots()
    sns.lineplot(data=points_season, x="year", y="points", marker="o", ax=ax)
    st.pyplot(fig)

    # Race finishes
    finish_counts = driver_data["positionOrder"].value_counts().sort_index()
    st.subheader("🏁 Finishing Positions")
    fig2, ax2 = plt.subplots()
    sns.barplot(x=finish_counts.index, y=finish_counts.values, ax=ax2)
    ax2.set_xlabel("Position")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

# -----------------------------------
# Tab 3: Driver Comparison
# -----------------------------------
with tab3:
    st.title("⚔️ Driver Comparison")

    col1, col2 = st.columns(2)
    with col1:
        driver1 = st.selectbox("Select First Driver", driver_names, key="driver1")
    with col2:
        driver2 = st.selectbox("Select Second Driver", driver_names, key="driver2")

    if driver1 == driver2:
        st.warning("Please select two different drivers for comparison.")
    else:
        d1_data = df[df["surname"] == driver1]
        d2_data = df[df["surname"] == driver2]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(driver1)
            image_path1 = Path(f"driver_images/{driver1.lower()}.png")
            if image_path1.exists():
                st.image(str(image_path1), width=200)
            st.markdown(f"**Races:** {len(d1_data)}")
            st.markdown(f"**Total Points:** {d1_data['points'].sum():.1f}")
            st.markdown(f"**Podiums (Top 3):** {(d1_data['positionOrder'] <= 3).sum()}")
            st.markdown(f"**Wins (1st place):** {(d1_data['positionOrder'] == 1).sum()}")

        with col2:
            st.subheader(driver2)
            image_path2 = Path(f"driver_images/{driver2.lower()}.png")
            if image_path2.exists():
                st.image(str(image_path2), width=200)
            st.markdown(f"**Races:** {len(d2_data)}")
            st.markdown(f"**Total Points:** {d2_data['points'].sum():.1f}")
            st.markdown(f"**Podiums (Top 3):** {(d2_data['positionOrder'] <= 3).sum()}")
            st.markdown(f"**Wins (1st place):** {(d2_data['positionOrder'] == 1).sum()}")

        # Points by Year Comparison
        st.subheader("📊 Points per Season Comparison")
        d1_season = d1_data.groupby("year")["points"].sum().reset_index()
        d2_season = d2_data.groupby("year")["points"].sum().reset_index()

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=d1_season, x="year", y="points", label=driver1, marker="o")
        sns.lineplot(data=d2_season, x="year", y="points", label=driver2, marker="o")
        plt.title("Points per Season")
        st.pyplot(fig)

        # Finishing Positions Histogram
        st.subheader("🏁 Finishing Position Distribution")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.histplot(d1_data["positionOrder"], bins=20, label=driver1, kde=False, color="blue", alpha=0.6)
        sns.histplot(d2_data["positionOrder"], bins=20, label=driver2, kde=False, color="red", alpha=0.6)
        plt.xlabel("Position Order")
        plt.ylabel("Frequency")
        plt.legend()
        st.pyplot(fig2)
