# Improving Elo
This is the code that I used for my Medium article [...] to rate college basketball teams from 2003 to 2019.

### Data
The data I use is based off of the dataset in this kaggle competition [...]. The columns are:  Season, DayNum, Winning Team, Winning Score, Losing Team, Losing Score. I included scores so that I can calculate the margin of victory. DayNum is day number of the season, and was just used so that I could track error over the course of the season. Unfortunately, as I don't want to upload the dataset, you'll have to supply your own data. If you are looking for the golf portion of the code, that can be found here [...]. In the case of golf, I released the scraper I used to gather data here [...].

### Packages
The only unusual package I use is TrueSkill, which can be found here [...]. TrueSkill is based off the Glicko system and I found that it didn't outperform it. Other packages are standard python data science packages, i.e. matplotlib.

### Running
The data path I used was './data/SeasonResults.csv'. Once data is loaded there, and you've either downloaded TrueSkill or scrubbed it from the code, it should be ready to go. Run ```main.py``` to get the results! I use ```settings.py``` to manipulate the parameters. Also, there are functions in the Elo class that are worth playing around with. For example, I used "k = 19.65 + math.exp((-.165*games_played)+3.45)" as my decay rate for K. Adjusting that function might improve results! It takes about 30 sec to calculate all 17 seasons on my laptop.

### Updating
Since I primarily just used this code for the Medium article, I won't update this regularly. Feel free to ask me any questions about anything you see. I tried to comment and write clear code, but I may have made a shortcut or two given that this was a solo project.
