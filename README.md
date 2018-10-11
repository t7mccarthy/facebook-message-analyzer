# facebook-message-analyzer
A Python script you can use to analyze your FB messages in 2018

In addition to the graphs plotting number of messages sent and words per message, I added a function that finds the most common word sent by each person in a conversation, and a function that analyzes the sentiment of a person's messages in a conversation.

For the most common word function, I looked at all of the words over length 3 (I didn't want boring words), and I only considered words made of alphabetic characters (the apostrophes were causing issues). I then found the most common word for each person in the conversation inputted (by looping through the list of words while comparing against each word).

For the sentiment analysis, I just used Textblob's sentiment method looking at the entirety of the >3 letter messages sent by a person in a conversation.
