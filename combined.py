import streamlit as st
import pandas as pd
import base64


def display_top_speed_app():
    st.title("Top Speeded Horses")
    uploaded_file = st.file_uploader("Upload CSV or XLSX file", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            display_top_speed(df)
        except Exception as e:
            try:
                df = pd.read_excel(uploaded_file)
                display_top_speed(df)
            except:
                st.write(f"Invalid file format. Error: {e}")
def display_official_rating_app():
    st.title("Official Rating Horses")
    uploaded_file = st.file_uploader("Upload CSV or XLSX file for Official Rating", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            display_official_rating(df)
        except Exception as e:
            try:
                df = pd.read_excel(uploaded_file)
                display_official_rating(df)
            except:
                st.write(f"Invalid file format. Error: {e}")

def display_top_speed(df):
    speed_column = 'Top Speed'
    df_top_speed = df[df[speed_column] != '-']
    df_top_speed = df_top_speed.dropna(subset=[speed_column])

    race_types_to_remove = ['Group 1', 'Group 2', 'Group 3', 'Handicap Chase', 'Handicap Hurdle', 'Maiden', 'NH Flat']
    df_top_speed = df_top_speed[~df_top_speed['Race Type'].isin(race_types_to_remove)]

    process_and_display(df_top_speed, speed_column, "Top Speeded Horses")


def display_official_rating(df):
    rating_column = 'Official Rating'
    df_rating = df[df[rating_column] != '-']
    df_rating = df_rating.dropna(subset=[rating_column])

    race_types_to_remove = ['Group 1', 'Claiming Stakes', 'Condition Stakes', 'Novice Stakes', 'Selling Stakes']
    df_rating = df_rating[~df_rating['Race Type'].isin(race_types_to_remove)]

    process_and_display(df_rating, rating_column, "Official Rating Horses")


def process_and_display(df, column_name, title):
    if len(df) > 0:
        df[column_name] = pd.to_numeric(df[column_name])
        top_horses = df.groupby('Race Name').apply(lambda x: x.loc[x[column_name].idxmax()]).reset_index(drop=True)
        top_horses = top_horses[['Time', 'Venue', 'Date', column_name, 'Race Type', 'Jockey', 'Trainer', 'Horse']]

        if len(top_horses) > 0:
            top_horses['Time'] = top_horses['Time'].astype(str)
            top_horses = top_horses.sort_values('Time')
            top_horses = top_horses[['Horse', 'Time', 'Venue', 'Date', column_name, 'Race Type', 'Jockey', 'Trainer']]
            st.dataframe(top_horses)

            csv_data = top_horses.to_csv(index=False)
            st.download_button(
                label=f"Download {title} CSV",
                data=csv_data,
                file_name=f"{column_name.lower().replace(' ', '_')}_horses.csv",
                mime='text/csv'
            )
        else:
            st.write(f"No horses found for {column_name}.")
    else:
        st.write(f"No data available for {column_name} horses.")


def filter_races_with_highest_rating(df):
    race_types = ['Handicap Chase', 'Handicap Hurdle', 'Maiden', 'Listed', 'Novice Stakes', 'N H Flat']
    max_ratings = df.groupby('Race Name')['RDB Rating'].transform('max')
    df_filtered = df[(df['RDB Rating'] == max_ratings) & (df['WFF Rank'] == 1) & (df['Race Type'].isin(race_types))]
    st.dataframe(df_filtered)

def filter_highest_rating_app():
    uploaded_file = st.file_uploader("Upload CSV or XLSX file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            filter_races_with_highest_rating(df)
        except Exception as e:
            try:
                df = pd.read_excel(uploaded_file)
                filter_races_with_highest_rating(df)
            except:
                st.write(f"Invalid file format. Error: {e}")

def main():
    st.title("Code Selection")
    code_selection = st.radio(
        "Select a code snippet",
        ["Display Top Speed Horses", "Display Official Rating Horses", "Filter Highest Rating Races"],
    )

    uploaded_file = st.file_uploader("Upload CSV or XLSX file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            try:
                df = pd.read_excel(uploaded_file)
            except:
                st.write(f"Invalid file format. Error: {e}")
                return

        if code_selection == "Display Top Speed Horses":
            display_top_speed(df)
        elif code_selection == "Display Official Rating Horses":
            display_official_rating(df)
        elif code_selection == "Filter Highest Rating Races":
            filter_races_with_highest_rating(df)
    else:
        st.write("Please upload a file to proceed.")


if __name__ == "__main__":
    main()
