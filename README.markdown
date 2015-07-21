# README

This is the code for MediaCloud's quarterback study, created by [Val Healy]( https://github.com/val1ant ).

## INSTALLATION

To install, first save the files in this repository.

### DEPENDENCIES

This program has several dependencies. You will need to have mediacloud (???) and nltk in order to run these scripts.

### HOW TO RUN

#### sentencedownload
Open up your virtual environment and run sentencedownload

#### tfidf
The tfidf script calculates and saves tfidf values from the files downloaded in executing the sentencedownload script. 
Therefore, you must run sentencedownload prior to running tfidf. 
You may run the tfidf script the same way as the sentencedownload script. 

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