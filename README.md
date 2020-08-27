# Who is the saltiest hacker? 
## An app that shows the saltiest commenters from Hacker News stories
## Data engineering by:
* Unit 3 - Jay Adamo, Brad Brauser & Ryan Koul
* Unit 4 - Rob Bennet & Hernan Echeverry
## Project Details
1. Utilizing a cleaned dataframe the team engineered a database consisting of 2 tables which held necessary data such as comment author and comment text.
2. With that information the team ran sentiment analysis rendering comments positive, neutral or negative.
3. A new feature was made called Saltiness that gave a numerical value that represented the level of saltiness of each commenter(ex. a value of -300 is very salty where 300 would be extremely positive.
4. The next step was to apply modeling and connecting to the database tables to organize the ranking of saltiness from most salty to least salty.
5. The final step was to allow a user to view the actual comments along with their saltiness score and rankings. 
6. The DS team then deployed an app to Heroku and passed on the information to the Web team.
### App deployed to: https://saltiest-hacker-news.herokuapp.com



