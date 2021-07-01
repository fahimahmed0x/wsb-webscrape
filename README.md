# About
This project webscrapes the post titles from the subreddit "WallStreetBets", and converts the data into a CSV file.
It also generates a graph containing the 10 most mentioned ticker symbols for that day.

![image](https://user-images.githubusercontent.com/68152521/124048193-c1f82200-d9e3-11eb-99c3-b0e2452e55d0.png)


# Usage
Run `pip3 install -r requirements.txt` in the terminal to install the required libraries.

Run webscrape.py to generate a CSV file. This CSV file contains tickers from post titles (ex. $AMD) and related post data from the current date.

Run wsb.Rmd in RStudio to generate a graph 
