**Motivation and purpose:**

Our role: Data Science Student Group

Target audience: Music enthusiasts (general population) and musicians

Spotify is a very large music platform with subscribers from all around the world. If we can understand what song qualities are associated with popularity in different genres, then this will provide valuable information to music creators. Furthermore, it may provide insights into the Spotify algorithm and how songs are ranked in terms of popularity. With this goal in mind, we will build an interactive visualization dashboard that will show how different song characteristics like energy and acousticness are related to song popularity within diffenent music genres. By using user interactions like filtering by genre, artist, or top ranking songs, we hope to elucidate some of these relationship between different song qualities. 

Description of Data

In our dashboard we will be visualizing around 30000 rows of data. Each of these rows corresponds to a song on a Spotify playist, and includes information including song name, artist, album, playlist genre, and various song qualities like energy, acousticness, danceability, liveness, speechiness, key, loudness, major/minor, instrumentalness, valence, tempo, and duration. The [dataset](https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-21) was provided on Github as the January 21, 2020 [Tidy Tuesday challenge](https://|github.com/rfordatascience/tidytuesday).

Research Questions and Usage Scenarios

1. To determine what makes a song popular based on the attributes present in the data. For instance, track_popularity, danceability, energy, key,loudness, mode, speechiness, acousticness, instrumentalness, etc. 
2. If we look at particular genres, how to these relationships change? For instance do the songs in a particular genre have identifying characteristics?
3. While the correlations between individual metrics and song popularity are quite small, how much of the variation in song popularity can be explained by these metrics if we use all of them as predictors in a linear regression?
4. Which artists and genres are most popular? 



