from streamlit import columns
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    # 1. fetch total number of messages
    num_messages= df.shape[0]

    #     2. fetch the total number of words
    words = []
    for i in df['message']:
        words.extend(i.split())

    # 3. fetch the number of media messages
    num_media_message=df[df['message']=="<Media omitted>\n"].shape[0]

    # 4. fetch the number of links shared
    links=[]
    for i in df['message']:
        links.extend(extract.find_urls(i))
    return num_messages, len(words),num_media_message,len(links)

def most_busy_user(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percentage'})
    return x,df

def create_wordcloud(selected_user,df):

    with open('stopwords.txt', 'r', encoding="utf-8") as f:
        stop_words = f.read()
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!="<Media omitted>\n"]

    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stopwords)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    with open('stopwords.txt', 'r', encoding="utf-8") as f:
        stop_words = f.read()
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!="<Media omitted>\n"]

    words=[]
    for i in temp['message']:
        for j in i.lower().split():
            if j not in stop_words:
                words.append(j)
    return_df=pd.DataFrame(Counter(words).most_common(20))
    return return_df

def emoji_func(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    emojis=[]
    for i in df['message']:
        emojis.extend([char for char in i if emoji.is_emoji(char)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])
    return emoji_df

def montly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    d_timeline=df.groupby('only_date').count()['message'].reset_index()
    return d_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()
