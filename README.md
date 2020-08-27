# Who is the saltiest hacker? 

## An app that shows the saltiest commenters from Hacker News stories
### Data engineering by: Jay Adamo, Brad Brauser & Ryan Koul
### Machine learning by: Rob Bennet & Hernan Echeverry
## Project Details
### 1. Utilizing a cleaned dataframe the team engineered a database consisting od a table which held necessary data such as comment author and comment text.
### 2. With that information the team ran sentiment analysis rendering comments positive, neutral or negative.
### 3. A new feature was made called Saltiness that gave a numerical value that represented the level of saltiness of each commenter
### 4. An additional table was added to the database that contained the saltiness values.
### 5. The next step was to apply modeling and connect to the database tables to organize the ranking of saltiness from most salty to least salty.
### 6. The final step was to write code that will allow a user to view the actual comments along with their saltiness scores and ranking. 
### 7. The DS team then deployed an app to Heroku and passed on the information to the Web team.
### App deployed to: https://saltiest-hacker-news.herokuapp.com

![Imgur](https://i.imgur.com/VmRC6Ak.png)

