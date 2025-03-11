import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import helper

st.set_page_config(layout="wide")  # Wide layout for better visualization

# Sidebar
st.sidebar.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("📂 Choose a File")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetching unique users
    user_list = df['user'].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show Analysis"):
        # Fetching statistics
        num_messages, words, media_share, num_link = helper.fetch_stats(selected_user, df)

        # Display statistics using Streamlit metrics
        st.title("📊 Key Statistics")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(label="📩 Total Messages", value=num_messages)
        col2.metric(label="📝 Total Words", value=words)
        col3.metric(label="📷 Media Shared", value=media_share)
        col4.metric(label="🔗 Links Shared", value=num_link)

        st.markdown("---")

        # Monthly Timeline
        st.title("📅 Monthly Timeline")
        timeline_df = helper.montly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=timeline_df, x='time', y='message', marker='o', linewidth=2.5, color="royalblue")
        plt.xticks(rotation=45, ha="right")
        ax.set_title("Messages Sent Over Time", fontsize=14, fontweight="bold")
        st.pyplot(fig)

        # Daily Timeline
        st.title("📆 Daily Timeline")
        d_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=d_timeline, x='only_date', y='message', linewidth=2.5, color="crimson")
        plt.xticks(rotation=45, ha="right")
        ax.set_title("Daily Messaging Pattern", fontsize=14, fontweight="bold")
        st.pyplot(fig)

        st.markdown("---")

        # Activity Map
        st.title("📍 Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("🗓️ Most Busy Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(busy_day.index, busy_day.values, color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("📅 Most Busy Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(busy_month.index, busy_month.values, color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown("---")

        # Most Busy Users
        if selected_user == "Overall":
            st.title("👥 Most Active Users")
            x, new_df = helper.most_busy_user(df)
            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(x.index, x.values, color="purple")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.markdown("---")

        # Word Cloud
        st.title("☁️ Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(df_wc, interpolation="bilinear")
        ax.axis("off")
        ax.set_title("Most Frequently Used Words", fontsize=14, fontweight="bold")
        st.pyplot(fig)

        st.markdown("---")

        # Most Common Words
        st.title("🗣️ Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(most_common_df[0], most_common_df[1], color="darkgreen")
        plt.xticks(rotation='vertical')
        ax.set_title("Top Words Used", fontsize=14, fontweight="bold")
        st.pyplot(fig)

        st.markdown("---")

        # Emoji Analysis
        emoji_df = helper.emoji_func(selected_user, df)
        st.title("😀 Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots(figsize=(6, 6))
                colors = sns.color_palette("pastel")
                ax.pie(
                    emoji_df['Count'].head(8),
                    labels=emoji_df['Emoji'].head(8),
                    autopct="%0.1f%%",
                    colors=colors,
                    startangle=140,
                    wedgeprops={"edgecolor": "black", "linewidth": 1}
                )
                ax.set_title("Top Used Emojis", fontsize=14, fontweight="bold")
                st.pyplot(fig)
            else:
                st.write("No emojis found in messages.")
