from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import requests
import smtplib

page = requests.get("https://www.sportsinteraction.com/soccer/england/premier-league-betting/")

soup = BeautifulSoup(page.content, 'html.parser')
matches = soup.find_all(class_="game")

def betting_odds(data):
    """Creates line of text with each team and their odds to win the game"""
    message = ''
    for games in data:
        teams = games.find_all(class_="name")
        odds = games.find_all(class_="price wide")
        if len(games.find_all(class_="date")) > 0:
             message += games.find(class_="date").get_text() + '\n'
        team1 = teams[0].get_text()
        draw = teams[1].get_text()
        team2 = teams[2].get_text()
        odds1 = odds[0].get_text()
        odds_draw = odds[1].get_text()
        odds2 = odds[2].get_text()
        message += "{}  {} \n{}  {} \n{}  {} \n".format(team1, odds1, draw, odds_draw, team2, odds2) + '\n'
    return message
    
fromx = 'email@site.com'
to = 'email@site.com'
msg = MIMEText('Here are the odds for the upcoming premier league games\n\n{}'.format(betting_odds(matches)))
msg['Subject'] = 'Premier League Odds'
msg['From'] = fromx
msg['To'] = to

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()

smtpObj.starttls()
smtpObj.login('email@site.com', 'Password')
smtpObj.sendmail(fromx, to, msg.as_string()) 
smtpObj.quit()

#loop through each div and take out text and add to list
#div - class = game (holds each match + odds + date if first match of the date)
#span - class = date (holds date, only located in first match of each day) 
#span - class = name (holds team name)
#span - class = price wide (holds odds)
