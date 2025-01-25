import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Page Configuration
st.set_page_config(
    page_title="Automotive Market Price Analytics", page_icon="🚗", layout="wide"
)


# --- Load and Preprocess Data ---
@st.cache_data
def load_car_data(file_path):
    try:
        with open(file_path, "r") as f:
            car_data_json = json.load(f)

        car_list = []
        for brand, models in car_data_json.items():
            # Skip if brand is a metadata field
            if brand in ["model", "price", "year"]:
                continue

            for model_info in models:
                car_list.append(
                    {
                        "Brand": brand.replace("_", " ").title(),
                        "Year": int(model_info["year"]),
                        "Model": model_info["model"],
                        "Price_str": model_info["price"],
                    }
                )

        car_df = pd.DataFrame(car_list)

        # Clean price data and convert to numeric
        car_df["Price"] = (
            car_df["Price_str"].replace({r"\$": "", ",": ""}, regex=True).astype(float)
        )  # Fixed SyntaxWarning using raw string
        car_df = car_df.drop("Price_str", axis=1)

        return car_df

    except FileNotFoundError:
        st.error(
            "Error: JSON file not found. Ensure the file is in the current directory."
        )
        return None


def main():
    st.title("Automotive Market Price Analytics")

    # Load Data
    car_df = load_car_data("complete.json")
    if car_df is None:
        return

    # --- Filters ---
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        # Brand Multiselect - Now defaults to all if none selected
        available_brands = sorted(car_df["Brand"].unique())
        selected_brands = st.multiselect(
            "Filter Automotive Brands (Leave empty to select all)",
            available_brands,
            default=[],  # Default is now an empty list
        )

        # If no brands selected, use all brands
        if not selected_brands:
            selected_brands = available_brands

    with col2:
        # Year Range Filter
        min_year = car_df["Year"].min()
        max_year = car_df["Year"].max()
        year_range = st.slider(
            "Model Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
        )

    with col3:
        # Price Range Filter
        min_price = int(car_df["Price"].min())
        max_price = int(car_df["Price"].max())
        price_range = st.slider(
            "Price Range ($)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
        )

    # --- Data Filtering ---
    filtered_df = car_df[car_df["Brand"].isin(selected_brands)]
    filtered_df = filtered_df[
        (filtered_df["Year"] >= year_range[0]) & (filtered_df["Year"] <= year_range[1])
    ]
    filtered_df = filtered_df[
        (filtered_df["Price"] >= price_range[0])
        & (filtered_df["Price"] <= price_range[1])
    ]

    # --- Visualizations ---
    if not filtered_df.empty:
        # Detailed Model Information (Moved to Top)
        st.subheader("Filtered Vehicle Models")

        # Add sorting option for Price
        sort_by_price = st.radio(
            "Sort Order by Price",
            options=["Ascending", "Descending"],
            horizontal=True,
            index=1,  # Set Descending as default
        )

        # Determine ascending or descending based on sort selection
        ascending_price = sort_by_price == "Ascending"

        model_display = (
            filtered_df[["Brand", "Year", "Model", "Price"]]
            .sort_values(
                by=["Price", "Brand", "Year", "Model"],
                ascending=[
                    ascending_price,
                    True,
                    True,
                    True,
                ],  # Sort Price based on radio input
            )
            .reset_index(drop=True)
        )

        # Apply price formatting after sorting
        model_display["Price"] = model_display["Price"].apply(lambda x: f"${x:,.2f}")
        st.dataframe(model_display, use_container_width=True)

        # Price Distribution Boxplot (Alphabetical Order)
        st.subheader("Price Distribution Across Brands (Alphabetical Order)")
        # Sort the DataFrame by 'Brand' alphabetically before plotting
        sorted_filtered_df_box = filtered_df.sort_values(by="Brand")
        fig_box = px.box(
            sorted_filtered_df_box,
            x="Brand",
            y="Price",
            title="Automotive Price Ranges by Brand (Alphabetical Order)",
            labels={"Price": "Price (USD)"},
            color="Brand",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            category_orders={"Brand": sorted_filtered_df_box["Brand"].unique()},
        )
        fig_box.update_layout(xaxis_tickangle=-45, title_font_size=16, title_x=0.5)
        st.plotly_chart(fig_box, use_container_width=True)

        # Average Price Bar Chart
        st.subheader("Average Price Comparison")
        avg_price_by_brand = (
            filtered_df.groupby("Brand")["Price"].mean().sort_values(ascending=False)
        )

        fig_bar = px.bar(
            x=avg_price_by_brand.index,
            y=avg_price_by_brand.values,
            title="Mean Automotive Prices by Brand",
            labels={"x": "Automotive Brand", "y": "Average Price (USD)"},
            color=avg_price_by_brand.index,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_bar.update_layout(yaxis_tickformat="$.2f", title_font_size=16, title_x=0.5)
        st.plotly_chart(fig_bar, use_container_width=True)

        # Brand-wise Price Summary (Maximized)
        st.subheader("Automotive Brand Price Analysis")
        brand_stats = filtered_df.groupby("Brand")["Price"].agg(
            ["count", "min", "max", "mean"]
        )

        brand_stats.columns = [
            "Model Count",
            "Minimum Price",
            "Maximum Price",
            "Average Price",
        ]

        def format_currency(x):
            if isinstance(x, (int, float)):
                return f"${x:,.2f}"
            return x

        brand_stats[["Minimum Price", "Maximum Price", "Average Price"]] = brand_stats[
            ["Minimum Price", "Maximum Price", "Average Price"]
        ].map(format_currency)
        st.dataframe(brand_stats, use_container_width=True)

    else:
        st.info(
            "No vehicle models match the current filter criteria. Adjust the filters above."
        )


# Run the app
if __name__ == "__main__":
    main()
