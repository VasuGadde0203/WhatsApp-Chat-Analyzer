import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob
from transformers import pipeline



st.sidebar.title("Whattsapp Chat Analyzer")


uplodaded_file = st.sidebar.file_uploader("Choose a file")
if uplodaded_file is not None:
    bytes_data = uplodaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    #fetch unique users 

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt ", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        
        with col4:
            st.header("Links shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)

        data = {'time': timeline['time'], 'message': timeline['message']}
        monthly_timeline_data = pd.DataFrame(data).set_index('time')
        st.bar_chart(monthly_timeline_data)


        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        st.line_chart(daily_timeline.set_index('only_date')['message'], use_container_width=True)


        # activity map 
        st.title('Activity map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            busy_day_df = busy_day.reset_index()
            busy_day_df.columns = ['Day', 'Activity']

            # Plot the bar chart using Streamlit's built-in function
            st.bar_chart(busy_day_df.set_index('Day')['Activity'])

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            busy_month_df = busy_month.reset_index()
            busy_month_df.columns = ['Month', 'Activity']

            # Plot the bar chart using Streamlit's built-in function
            st.bar_chart(busy_month_df.set_index('Month')['Activity'])

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # Most busy users
        if selected_user == 'Overall':
            most_messages_user = helper.most_busy_users(df)
            st.title("Most number of messages by Users")

            col1, col2 = st.columns(2)

            with col1:
                busy_users = most_messages_user.head()
                busy_users_df = busy_users.set_index('user')['count']
                st.bar_chart(busy_users_df, color='#ffaa00')
            with col2: 
                st.dataframe(most_messages_user)

        # WordCloud 
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words 
        most_common_df = helper.most_common_words(selected_user, df)
        most_common_df.columns = ['Word', 'Count']
        # Create a horizontal bar chart using Plotly
        fig = px.bar(most_common_df, y='Word', x='Count', orientation='h', color='Count', color_continuous_scale='Blues')
        # Update layout for better readability
        fig.update_layout(
            xaxis_title='Count',
            yaxis_title='Word',
            title='Most Common Words'
        )
        # Display the plot in Streamlit
        st.plotly_chart(fig)


        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            emoji_df.columns = ['Emoji', 'Count']
            # Create a pie chart using Plotly
            fig = px.pie(emoji_df.head(), names='Emoji', values='Count', 
                        title='Emoji Distribution')
            # Update layout for better readability
            fig.update_layout(
                legend_title='Emoji',
                title='Emoji Distribution'
            )
            # Display the plot in Streamlit
            st.plotly_chart(fig)


        # Sentiment Analysis
        st.title("Sentiment Analysis")
        sentiment_df = helper.sentiment_analysis(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(sentiment_df.rename_axis('index'))
        with col2:
            st.line_chart(sentiment_df['sentiment'])
        

        # Response Time Analysis
        st.title("Average Response Time (minutes)")
        if selected_user == 'Overall':
            response_df = df[df['user'] != df['user'].shift(-1)]
        else:
            response_df = df[(df['user'] != df['user'].shift(-1)) & (df['user'] == selected_user)]
        
        avg_response_time = response_df.groupby('user')['response_time'].mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(avg_response_time.sort_values())
        with col2:
            st.bar_chart(avg_response_time)

        # Time of Day Analysis
        st.title("Messages by Time of Day")
        if selected_user == 'Overall':
            df_time = df
        else:
            df_time = df[df['user'] == selected_user]

        time_distribution = df_time.groupby('hour').size()
        st.line_chart(time_distribution)
        st.write("This chart shows the number of messages sent during each hour of the day.")


        # Topic Modeling
        st.title("Topic Modeling")
        if selected_user == 'Overall':
            df_topic = df
        else:
            df_topic = df[df['user'] == selected_user]
        
        # Vectorizing the text data
        vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
        X = vectorizer.fit_transform(df_topic['message'])
        
        # LDA Model
        lda = LatentDirichletAllocation(n_components=5, random_state=42)
        lda.fit(X)
        
        cols = st.columns(5)  
        # Display topics
        for idx, topic in enumerate(lda.components_):
            if idx < len(cols):
                col = cols[idx]
                with col: 
                    st.write(f"**Topic {idx + 1}:**")
                    st.write([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]])

        

        