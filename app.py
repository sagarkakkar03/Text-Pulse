import nltk
import streamlit as st
import pandas as pd
import preprocessor
import Helper
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu
import streamlit as st
import streamlit.components.v1 as com
nltk.downloader.download('vader_lexicon')
st.sidebar.header('Whatsapp Bussiness Visualizer')


st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 375px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)
uploaded_file = st.sidebar.file_uploader("Choose a file")
with st.sidebar:
    selected = option_menu(menu_title='',
                           options=['User', 'Timeline','Words', "Emoji", 'Wordcloud', 'Contribution'])
# Main heading
st. markdown("<h1 style='text-align: center; color: #26495c;'>Whatsapp Bussiness Visualizer</h1>", unsafe_allow_html=True)
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # yeh data byte data ka stream hai isse string mein convert krna pdeega
    data = bytes_data.decode('utf-8')
    # ab file ka data screen pe dikhne lagega
    df = preprocessor.preprocess(data)
    df2 = preprocessor.preprocess2(data)
    df3 = preprocessor.preprocess3(data)
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    def sentiment(d):
        if d["pos"] >= d["neg"] and d["pos"] >= d["nu"]:
            return 1
        if d["neg"] >= d["pos"] and d["neg"] >= d["nu"]:
            return -1
        if d["nu"] >= d["pos"] and d["nu"] >= d["neg"]:
            return 0


    # Object
    sentiments = SentimentIntensityAnalyzer()
    df["pos"] = [sentiments.polarity_scores(i)["pos"] for i in df["message"]]  # Positive
    df["neg"] = [sentiments.polarity_scores(i)["neg"] for i in df["message"]]  # Negative
    df["nu"] = [sentiments.polarity_scores(i)["neu"] for i in df["message"]]
    df['value'] = df.apply(lambda row: sentiment(row), axis=1)
    st.dataframe(df)


    # fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('show analysis wrt', user_list)
    if st.sidebar.button('Show Analysis'):
        num_messages, words, num_media_messages, num_of_links = Helper.fetch_stats(selected_user, df2)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("<h2 style='text-align: left; color = #26495C;border-style: solid;'>Total Messages</h2>",unsafe_allow_html=True)
            st.title(num_messages)
        with col2:
            st.markdown("<h2 style='text-align: left; color = #26495C;border-style: solid;'>Total Words</h2>", unsafe_allow_html=True)

            #st.markdown('<p class="big-font">Total  Words </p>', unsafe_allow_html=True)
            st.title(words)
        with col3:

            st.markdown("<h2 style='text-align: left; color = #26495C;border-style: solid;'>Media Messages</h2>", unsafe_allow_html=True)
            st.title(num_media_messages)
        with col4:
            st.markdown("<h2 style='text-align: left; color = #26495C;border-style: solid;'>Links Shared</h2>",unsafe_allow_html=True)
            st.title(num_of_links)

        #timeline
        # monthly
        if selected == 'Timeline':
            col1, col2 = st.columns(2)
            with col1:
                timeline = Helper.monthly_timeline(selected_user, df)
                fig = px.line(timeline , x = 'time', y = 'message' , title = 'User Activity Monthly',
                 width=400, height=400)

                fig
            # daily
            with col2:
                timeline = Helper.day_timeline(selected_user, df)
                fig = px.line(timeline, x='day_name', y='message', title='User Activity DayWise',
                 width=400, height=400)
                fig
        # finding the busiest users in the group (Group - level)
        if selected == 'User':
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x, new_df = Helper.most_busy_users(df)
                fig, ax = plt.subplots()
                #col1, col2 = st.columns(2)
                names = new_df['names']
                percentage = new_df['percentage']
                fig = px.bar(new_df, x=names, y=percentage, color=names)
                fig

        # WordCloud
        if selected == 'Wordcloud':
            df_wc = Helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            plt.imshow(df_wc)
            st.pyplot(fig)
        if selected == "Contribution":
        # Most Positive, Negitive, Neutral user...
            if selected_user == 'Overall':
            #    col1, col2, col3 = st.columns(3)
            #    with col1:
                    st.markdown("<h3 style='text-align: center; color: orange;'>Most Positive Users</h3>",unsafe_allow_html=True)
                    af = df['user'][df['value'] == 1]
                    x = af.value_counts()
                    fig = px.bar(af, y=x.values, x=x.index, color=x)
                    fig
            #    with col2:
                    st.markdown("<h3 style='text-align: center; color: blue;'>Most Neutral Users</h3>",unsafe_allow_html=True)
                    af = df['user'][df['value'] == 0]
                    x = af.value_counts()
                    fig = px.bar(af, y=x.values, x=x.index, color=x)
                    fig
            #    with col3:
                    st.markdown("<h3 style='text-align: center; color: green;'>Most Negitive Users</h3>",unsafe_allow_html=True)
                    af = df['user'][df['value'] == -1]
                    x = af.value_counts()
                    fig = px.bar(af, y=x.values, x=x.index, color=x)
                    fig
        # most common words
        if selected == 'Words':
            #col1, col2, col3 = st.columns(3)

            #with col1:
                try:
                    st.markdown("<h3 style='text-align: center; color: orange;'>Most Positive Words</h3>",
                                unsafe_allow_html=True)
                    most_common_df = Helper.most_common_words(selected_user, df, 1)
                    fig, ax = plt.subplots()
                    word = most_common_df['word']
                    number = most_common_df['number']
                    fig = px.bar(most_common_df, y=number, x=word, color=word)
                    fig
                except:
                    pass
            #with col2:
                try:
                    st.markdown("<h3 style='text-align: center; color: blue;'>Most Neutral words</h3>",
                                unsafe_allow_html=True)
                    most_common_df = Helper.most_common_words(selected_user, df, 0)
                    word = most_common_df['word']
                    number = most_common_df['number']
                    fig = px.bar(most_common_df, y=number, x=word, color=word)
                    fig
                except:
                    pass
            #with col3:
                try:
                    st.markdown("<h3 style='text-align: center; color: green;'>Most Negitive words</h3>",
                                unsafe_allow_html=True)
                    most_common_df = Helper.most_common_words(selected_user, df, -1)
                    fig, ax = plt.subplots()
                    word = most_common_df['word']
                    number = most_common_df['number']
                    fig = px.bar(most_common_df, y=number, x=word, color=word)
                    fig
                except:
                    pass
        # emoji analysis
        if selected == 'Emoji':
            try:
                emoji_df, p, neg, nu = Helper.emoji_helper(selected_user, df)
                st.title("Emoji Analysis")
                col1, col2, col3 = st.columns(3)
                with col1:
                    try:
                        st.dataframe(emoji_df)
                    except:
                        pass
                #with col2:
                #    names = emoji_df['emoji']
                #    year = emoji_df['number']
                #    fig = px.pie(emoji_df, values=year, names= names)
                #    fig.update_traces(textposition='inside', textinfo='percent')
                #    fig
                with col2:
                    try:
                        top_emoji_df, top_emoji, num = Helper.top_emoji(selected_user, emoji_df)
                        st.dataframe(top_emoji_df, width=40, height=400)
                    except:
                        pass
                with col3:
                    try:
                        top_emoji_df, top_emoji, num = Helper.top_emoji(selected_user, emoji_df)
                        arr = [int((p / (p + neg + nu)) * 100), int((neg / (p + neg + nu)) * 100),
                               int((nu / (p + neg + nu)) * 100)]
                        af = pd.DataFrame({'sentiment': ['positive', 'negitive', 'neutral'], 'percentage': arr, 'top_emoji':top_emoji})
                        fig = px.pie(af, values='percentage', names='sentiment',hover_data=['top_emoji'] ,labels={'top_emoji':'top_emoji' })
                        fig.update_traces(textposition='inside', textinfo='percent')
                        fig
                    except:
                        try:
                            arr = [int((p/(p+neg+nu))*100), int((neg/(p+neg+nu))*100), int((nu/(p+neg+nu))*100)]
                            af = pd.DataFrame({'sentiment': ['positive', 'negitive', 'neutral'], 'percentage': arr})
                            fig = px.pie(af, values='percentage', names='sentiment')
                            fig.update_traces(textposition='inside', textinfo='percent')
                            fig
                        except:
                            pass
            except:
                pass