##Extract tweets from the file manually downloaded from Twitter Analytics##

import pandas as pd

##############################################################################
#
#read file with all the tweets from january 2021 to june 2022, downloaded from Twitter Analytics
df = pd.read_csv('./twitter_analysis/tweets_johd.csv')
#
##############################################################################
print(df)
#
##############################################################################
#
#list of hashtags to divide the tweets in different files based on the hashtag used
#
##############################################################################
#
hashtags = ["#showmeyourdata", "#johdnews", "#johdagenda", "#johdsuggestions", "#johdpapers"]
#
##############################################################################
#select_hashtag = df.loc[df['Tweet text'].str.contains("|".join(hashtags))]
#select_hashtag = df.loc[df['Tweet text'].str.contains("#showmeyourdata")]
#
###################################################
#
#look for each hashtag in the column named 'Tweet text'
#
##############################################################################
showmeyourdata = df.loc[df['Tweet text'].str.contains("#showmeyourdata")]
johdpapers = df.loc[df['Tweet text'].str.contains("#johdpapers")]
johdnews = df.loc[df['Tweet text'].str.contains("#johdnews")]
johdagenda = df.loc[df['Tweet text'].str.contains("#johdagenda")]
johdsuggestions = df.loc[df['Tweet text'].str.contains("#johdsuggestions")]
#
#
#############################################################################
#
#print tweets containing each hashtag in a different file
#
#############################################################################

showmeyourdata.to_csv("./twitter_analysis/tweets_by_hashtag/#showmeyourdata.csv")
johdpapers.to_csv("./twitter_analysis/tweets_by_hashtag/#johdpapers.csv")
johdnews.to_csv("./twitter_analysis/tweets_by_hashtag/#johdnews.csv")
johdagenda.to_csv("./twitter_analysis/tweets_by_hashtag/#johdagenda.csv")
johdsuggestions.to_csv("./twitter_analysis/tweets_by_hashtag/#johdsuggestions.csv")
#
###############################################################################
#FOLLOWING COMMENTED OUT: the analysis on engagement rates does not give significant results
#
#copy engagement rate to another csv called "test_new" to perform statistics
#
##############################################################################
#df_show = pd.read_csv("./twitter_analysis/tweets_by_hashtag/#showmeyourdata.csv")
#df_papers = pd.read_csv("./twitter_analysis/tweets_by_hashtag/#johdpapers.csv")
#df_news = pd.read_csv("./twitter_analysis/tweets_by_hashtag/#johdnews.csv")
#df_agenda = pd.read_csv("./twitter_analysis/tweets_by_hashtag/#johdagenda.csv")
#df_suggestions = pd.read_csv("./twitter_analysis/tweets_by_hashtag/#johdsuggestions.csv")
# engrate_show = df_show[["engagement rate"]]
# test_new = engrate_show.copy()
# print(test_new)


#test_new = pd.DataFrame()
#test_new['engrate_show'] = df_show[["engagement rate"]].copy()
#test_new['engrate_papers'] = df_papers[["engagement rate"]].copy()
#test_new['engrate_news'] = df_news[["engagement rate"]].copy()
#test_new['engrate_agenda'] = df_agenda[["engagement rate"]].copy()
#test_new['engrate_suggestions'] = df_suggestions[["engagement rate"]].copy()

#test_new.to_csv("/home/sitel/Téléchargements/tweet_activity/test_new.csv")
