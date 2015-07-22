# README

This is the code for MediaCloud's quarterback study, created by [Val Healy]( https://github.com/val1ant ).

## INSTALLATION

To install, save this repository's files to your computer.
Open the config file (config.txt) and paste in your API key where indicated. Don't have a MediaCloud API key? Register to get yours [here]( https://core.mediacloud.org/login/register ) and see yours [here]( https://core.mediacloud.org/admin/profile ).
Then, install the dependencies listed below.

### DEPENDENCIES

This program has several dependencies. You will need to have the [MediaCloud API client]( https://github.com/c4fcm/MediaCloud-API-Client ) and the [Natural Language Toolkit]( http://www.nltk.org/ ) in order to run these scripts.
You will also need to download and save MediaMeter's [stopwords script]( https://github.com/c4fcm/Global-Coverage-Study/blob/master/media-source-dashboard/mediameter/stopwords.py#L17 ) and [stopword list]( https://raw.githubusercontent.com/c4fcm/Global-Coverage-Study/master/json-generator/stop-words-english4.txt ).

### HOW TO RUN

#### sentencedownload
Open up your virtual environment in terminal and run sentencedownload.py.

#### tfidf
The tfidf script calculates and saves tfidf values from the files downloaded in executing the sentencedownload script. 
Therefore, you must run sentencedownload prior to running tfidf. 
Open up your virtual environment in terminal and run tfidf.py.

### METHODOLOGY

#### Quarterbacks
To acquire the information (name and team) for each quarterback, I used the Wikipedia [list of starting quarterbacks]( https://en.wikipedia.org/wiki/List_of_NFL_starting_quarterbacks ).
For each team in the table, I found the list of each team's 2014 starting quarterbacks by clicking *(list)* next to each team in the table. 

#### Race Determination
Race determination is a tricky and difficult task. Ideally, I would categorize using each player's self-identified race.
However, I was unable to find evidence of self-identification for any of the players.
Thus, for this project, I elected to use the categorizations found in [Best Ticket's unofficial 2014 NFL Player Census]( http://www.besttickets.com/blog/nfl-player-census-2014/ ).
Their methodology is as follows:
Several players () were not included in this list; I used the same methodology to categorize these players.