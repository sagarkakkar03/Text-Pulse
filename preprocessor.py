def preprocess(data):
    import re
    import pandas as pd
    pattern = '\d{1,2}/\d{1,2}/\d{2,4}\,\s\d{1,2}\:\d{1,2}\s\w\w\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'messages_date': dates})
    df['messages_date'] = pd.to_datetime(df['messages_date'], dayfirst=False)
    df.rename(columns={'messages_date': 'Date'}, inplace=True)
    users = []
    messages = []
    #special character removal
    for message in df['user_message']:
        entry = re.split('\-\ ([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    special_characters = '''!()-[]{};:'"|\,<>./?@#$%^&*+_'''
    new_messages = []
    for i in range(len(messages)):
        new_string = ''
        for j in messages[i]:
            if j not in special_characters:
                new_string = new_string+j
            else: new_string += ' '
        new_messages.append(new_string)
    #df = df[df['message'] != '\n']
    df['user'] = users
    df['message'] = new_messages
    df.drop(columns=['user_message'], inplace=True)
    df = df[df['message'] != ' Media omitted \n']
    df = df[df['message'] != ' \n']
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month_name()
    df['month_num'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    return df
def preprocess2(data):
    import re
    import pandas as pd
    pattern = '\d{1,2}/\d{1,2}/\d{2,4}\,\s\d{1,2}\:\d{1,2}\s\w\w\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'messages_date': dates})
    df['messages_date'] = pd.to_datetime(df['messages_date'], dayfirst=False)
    df.rename(columns={'messages_date': 'Date'}, inplace=True)
    users = []
    messages = []
    #special character removal
    for message in df['user_message']:
        entry = re.split('\-\ ([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    #df = df[df['message'] != '\n']
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df = df[df['message'] != ' Media omitted \n']
    df = df[df['message'] != ' \n']
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month_name()
    df['month_num'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    return df
def preprocess3(data):
    import re
    import pandas as pd
    import emoji
    pattern = '\d{1,2}/\d{1,2}/\d{2,4}\,\s\d{1,2}\:\d{1,2}\s\w\w\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'messages_date': dates})
    df['messages_date'] = pd.to_datetime(df['messages_date'], dayfirst=False)
    df.rename(columns={'messages_date': 'Date'}, inplace=True)
    users = []
    messages = []
    #special character removal
    for message in df['user_message']:
        entry = re.split('\-\ ([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    special_characters = '''!()-[]{};:'"|\,<>./?@#$%^&*+_'''
    new_messages = []
    emojis = []
    for message in df['user_message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    for i in range(len(messages)):
        new_string = ''
        for j in messages[i]:
            if j not in special_characters and j not in emojis:
                new_string = new_string+j
            else: new_string += ''
        if new_string!= '':
            new_messages.append(new_string)
    #df = df[df['message'] != '\n']
    df['user'] = users
    df['message'] = new_messages
    df.drop(columns=['user_message'], inplace=True)
    df = df[df['message'] != ' Media omitted \n']
    df = df[df['message'] != ' \n']
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month_name()
    df['month_num'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    return