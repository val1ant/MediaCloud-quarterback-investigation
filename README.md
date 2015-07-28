# README

This is the code for MediaCloud's quarterback study, created by [Val Healy]( https://github.com/val1ant ).

## INSTALLATION

To install, save this repository to your computer.
Copy the `config.txt.template` to `config.txt` and then paste in your API key where indicated. Don't have a MediaCloud API key? Register to get yours [here]( https://core.mediacloud.org/login/register ) and see your API key [here]( https://core.mediacloud.org/admin/profile ).
Then, install the dependencies listed below.

### DEPENDENCIES

This program has several dependencies. You will need to have the [MediaCloud API client]( https://github.com/c4fcm/MediaCloud-API-Client ), the [Natural Language Toolkit]( http://www.nltk.org/ ), and [unicodecsv]( https://pypi.python.org/pypi/unicodecsv ) in order to run these scripts. [scipy]( http://www.scipy.org/ ) is optional.

```shell
pip install -r requirements.pip
```

### HOW TO RUN

#### sentencedownload
Open up your virtual environment in terminal and run sentencedownload.py.

#### tfidf
The tfidf script calculates and saves tfidf values from the files downloaded in executing the sentencedownload script. 
Therefore, *you must run sentencedownload prior to running tfidf*. 
Open up your virtual environment in terminal and run tfidf.py.

### METHODOLOGY

#### Quarterbacks
To acquire the information (name and team) for each quarterback, I used the Wikipedia [list of starting quarterbacks]( https://en.wikipedia.org/wiki/List_of_NFL_starting_quarterbacks ).
For each team in the table, I found the list of each team's 2014 starting quarterbacks by clicking **(list)** next to each team in the table. 

#### Race Determination
Race determination is a tricky and difficult task. Ideally, I would categorize using each player's self-identified race.
However, I was unable to find evidence of self-identification for any of the players.
Thus, for this project, I elected to use the categorizations found in [Best Ticket's unofficial 2014 NFL Player Census]( http://www.besttickets.com/blog/nfl-player-census-2014/ ).
Their methodology is as follows:
```
Though not quite as diverse as leagues like the NBA or the MLB, the NFL is composed of a wide variety of players. Using the eye test, and clues like last name and birthplace, we classified each NFL player. Our racial classifications are as follows:
-Black
-White
-Hispanic
-Other
-Asian/Pacific Islander
The “Other” category consists of players of mixed racial composition and players whose racial categories only consisted of one or two instances. 
```
I used this same methodology to categorize the following players who were not found in the Best Ticket list above:
-Ryan Lindley (Arizona Cardinals)
-Connor Shaw (Cleveland Browns)
-Case Keenum (Houston Texans)