import os
import json
import numpy as np
import pylab as pl
import datetime
from textblob import TextBlob

CURRENT_DIRECTORY = os.getcwd()
NUMBER_TO_ANALYZE = 10000
MESSAGE_THRESHOLD = 100

def get_json_data(chat):
    try:
        json_location = CURRENT_DIRECTORY + "/messages/" + chat + "/message.json"
        with open(json_location) as json_file:
            json_data = json.load(json_file)
            return json_data
    except IOError:
        pass # some things the directory aren't messages (DS_Store, stickers_used, etc.)

chats = os.listdir(CURRENT_DIRECTORY + "/messages")[:NUMBER_TO_ANALYZE]
sorted_chats = []
final_data_messages = {}
final_data_times = {}
final_data_num_words = {}
final_data_words = {}
invalid_message_count = 0

print('Analyzing ' + str(min(NUMBER_TO_ANALYZE, len(chats))) + ' chats...')

for chat in chats:
    json_data = get_json_data(chat)
    if json_data != None:
        messages = json_data["messages"]
        if len(messages) >= MESSAGE_THRESHOLD:
            sorted_chats.append((len(messages), chat, messages))

sorted_chats.sort(reverse=True)

print('Finished processing chats...')

for i, (messages, chat, messages) in enumerate(sorted_chats):
    number_messages = {}
    person_to_times = {}
    number_words = {}
    words = {}

    print(str(i) + " - " + str(len(messages)) + " messages - " + str(chat))

    for message in messages:
        try:
            name = message["sender_name"]
            time = message["timestamp_ms"]
            message_content = message["content"]

            number_messages[name] = number_messages.get(name, 0)
            number_messages[name] += 1

            person_to_times[name] = person_to_times.get(name, [])
            person_to_times[name].append(datetime.datetime.fromtimestamp(time/1000.0))

            number_words[name] = number_words.get(name, [])
            number_words[name].append(len(message_content.split()))

            words[name] = words.get(name, [])
            temp = message_content.split()
            for word in temp:
                if(word.isalpha() and len(word) > 4):
                    words[name].append(word)
            #words[name].append(message_content.split())
        except KeyError:
            # happens for special cases like users who deactivated, unfriended, blocked
            invalid_message_count += 1

    final_data_messages[i] = number_messages
    final_data_times[i] = person_to_times
    final_data_num_words[i] = number_words
    final_data_words[i] = words

print('Found ' + str(invalid_message_count) + ' invalid messages...')
print('Found ' + str(len(sorted_chats)) + ' chats with ' + str(MESSAGE_THRESHOLD) + ' messages or more')

def plot_num_messages(chat_number):
    plotted_data = final_data_messages[chat_number]
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Number of Messages Sent')
    pl.tight_layout()
    pl.show()

def plot_histogram_words(chat_number):
    temp = {}
    for person in final_data_num_words[chat_number]:
        temp[person] = np.average(final_data_num_words[chat_number][person])
    plotted_data = temp
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Average Word Count')
    pl.tight_layout()
    pl.show()

def most_common_words(chat_number):
    print("\nMost Common Words:")
    for person in final_data_words[chat_number]:
        count = 0
        tempcount = 0
        words = final_data_words[chat_number][person]
        for word in words:
            for another in words:
                if(word == another):
                    tempcount += 1
            if(tempcount > count):
                count = tempcount
                result = word
            tempcount = 0
        print(person+": "+result)

def sentiment_analysis(chat_number):
    print("\nSentiment Analysis:")
    for person in final_data_words[chat_number]:
        count = 0
        tempcount = 0
        sentiment = get_sentiment(" ".join(final_data_words[chat_number][person]))
        print(person+": "+sentiment)

def get_sentiment(mess):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(mess)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'



def plot(chat_number):
    plot_num_messages(chat_number)
    plot_histogram_words(chat_number)

plot(18)
most_common_words(18)
sentiment_analysis(18)
