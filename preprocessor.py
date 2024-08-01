import re 
import pandas as pd 

def preprocess(data):

    if ('am' in data[1:19]) or ('pm' in data[1:19]):
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[apmAPM]{2}\s-\s'
    else:    
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_data': dates})

    if ('am' in data[1:19]) or ('pm' in data[1:19]):
        df['message_data'] = pd.to_datetime(df['message_data'], format='%d/%m/%y, %I:%M %p - ')

    else:
        df['message_data'] = pd.to_datetime(df['message_data'], format= '%d/%m/%y, %H:%M - ')

    df.rename(columns = {'message_data':'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notofication')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns = ['user_message'], inplace=True)

    df = df[df['user'] != 'group_notofication']
    df = df[df['message'] != '']
    # df = df[~df['message'].str.contains('<Media omitted>')]
    df = df[df['message'] != 'This message was deleted\n']
    df['message'] = df['message'].str.replace('<This message was edited>', '')
    df = df[df['message'] != 'null\n']
    df = df.reset_index()

    df['only_date'] = df['date'].dt.date 
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month 
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period 

    # Calculate response time
    df['next_message_time'] = df['date'].shift(-1)
    df['response_time'] = (df['next_message_time'] - df['date']).dt.total_seconds() / 60.0

    return df 

    