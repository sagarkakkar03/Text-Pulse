from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import nltk
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        # 1. number of messages
    extractor = URLExtract()
    urls = extractor.find_urls("Let's www.gmail.com have URL stackoverflow.com as an example google.com, http://facebook.com, ftp://url.in")
    y = []
    for message in df['message']:
        y.extend(extractor.find_urls(message))
    num_of_links = len(y)
    num_messages = df.shape[0]
    # 2. Number of words
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    return num_messages, len(words), num_media_messages, num_of_links
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns = {'index': 'names', 'user': 'percentage'})
    return x, df
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)
    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc
def most(df, k):
    df = df['user'][df['value'] == k]
    x = df.value_count().head(10)
    return x
def most_common_words(selected_user, df, k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import emoji
    from collections import Counter
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and word not in emojis:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common())
    number = []
    for message in most_common_df[1]:
        number.append(str(message))
    most_common_df['number'] = number
    most_common_df.rename(columns={0: 'word'}, inplace=True)
    del most_common_df[1]
    sentiments = SentimentIntensityAnalyzer()
    most_common_df["pos"] = [sentiments.polarity_scores(i)["pos"] for i in most_common_df["word"]]  # Positive
    most_common_df["neg"] = [sentiments.polarity_scores(i)["neg"] for i in most_common_df["word"]]  # Negative
    most_common_df["nu"] = [sentiments.polarity_scores(i)["neu"] for i in most_common_df["word"]]
    if k == 0:
        df = most_common_df[most_common_df['nu'] == 1].head(20)
    elif k == 1:
        df = most_common_df[most_common_df['pos'] == 1].head(20)
    else:
        df = most_common_df[most_common_df['neg'] == 1].head(20)
    return df
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    number = []
    text = []
    for emo in emoji_df[0]:
        text.append(emoji.demojize(emo))
    for message in emoji_df[1]:
        number.append(str(message))
    emoji_df['number'] = number
    emoji_df['emo'] = text
    emoji_df.rename(columns={0: 'emoji'}, inplace=True)
    positive = ['😂', '👍', '✌', '🔥', '🤣', '🙂', '✨', '❤', '😄', '😌', '🥳', '😎', '😁', '🫂', '😇', '🗿', '👌', '🙌',
                '😳', '😗', '😘']
    negitive = ['🥲', '😭', '🤦', '😔', '😤', '😑', '🤧', '😓', '😩', '😬', '😢', '🤨', '🤓', '🙄', '😥', '🥱', '😞',
                '😖', '💔', '😒']
    neutral = ['🥺', '♀', '🌝', '😅', '🫡', '🙏', '🙃', '🤔', '🌧', '♂', '🌚', '😶', '🤌', '⛈', '👀', '😈', '🌫', '🤷',
               '🤝', '😏', '🌩', '😒', '☔', '😝']
    p = 0
    neg = 0
    nu = 0
    for i in emojis:
        if i in positive:
            p+=1
        elif i in negitive:
            neg += 1
        else:
            nu += 1
    table = []
    for i in emoji_df['emoji']:
        if i in positive:
            table.append(1)
        elif i in negitive:
            table.append(-1)
        else:
            table.append(0)
    del emoji_df[1]
    emoji_df['value'] = table
    return emoji_df, p, neg, nu
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def top_emoji(selected_user, emoji_df):
    positive_df = emoji_df['emoji'][emoji_df['value'] == 1]
    p_count = 0
    arr = []
    num = []
    string = ''
    x = min(3, int(positive_df.shape[0]))
    count = 0
    for i in positive_df:
        if count == x:
            break
        af = emoji_df[emoji_df['emoji'] == i]
        p_count += int(af['number'])
        string += i
        count += 1
    arr.append(string)
    num.append(p_count)
    negitive_df = emoji_df['emoji'][emoji_df['value'] == -1]
    string = ''
    x = min(3, int(negitive_df.shape[0]))
    n_count = 0
    count = 0
    for i in negitive_df:
        if count == x:
            break
        string += i
        af = emoji_df[emoji_df['emoji'] == i]
        n_count += int(af['number'])
        count += 1
    arr.append(string)
    num.append(n_count)
    neutral_df = emoji_df['emoji'][emoji_df['value'] == 0]
    string = ''
    x = min(3, int(neutral_df.shape[0]))
    nu_count = 0
    count = 0
    for i in neutral_df:
        if count == x:
            break
        af = emoji_df[emoji_df['emoji'] == i]
        nu_count += int(af['number'])
        string += i
        count += 1
    arr.append(string)
    num.append(nu_count)
    df = pd.DataFrame({'emoji': arr, 'count': num})
    return df, arr, num
def day_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['day_name']).count()['message'].reset_index()
    return timeline
