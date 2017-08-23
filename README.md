# pyscrape
Quick and dirty python script to scrape craigslist for certain results in a certain price range
Parses through the return of a cURL to find items matching your price range, compiles them into json and emails a digest.

Use with crontab to make run every x days.

# To Run
python cl_scrape.py --queries [list of queries] --prices [list of max prices for queries]

*To make run with multiple queries and prices, but the main code in a loop over queires and prices -- was too lazy to implement that myself fully*

# Set Up
Global variables initialized to garbage, change the email, to, pass, etc fields to your email, pass, etc.
