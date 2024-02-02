import requests
from bs4 import BeautifulSoup
import csv
from flask import Flask, render_template

app = Flask(__name__)

headlines = []
links = []

def extract_data():
    article_year = 2024
    base_url = "https://www.theverge.com/archives"

    while article_year >= 2022 :
        page_url = f"{base_url}/{article_year}/1"
        html_text = requests.get(page_url)
        soup = BeautifulSoup(html_text.content, "lxml")
        
        articles = soup.find_all('h2', class_ = "c-entry-box--compact__title")
        
        for elements in articles:
            # Check for missing elements before extracting links
            if elements.find('a'):
                headline = elements.find('a').text.strip()
                article_url = elements.find('a')["href"]
                print(headline)
                print(article_url)
                headlines.append(headline)
                links.append(article_url)
            else:
                print("Article link not found in this element.")

        article_year = article_year - 1
        
    with open("headlines.csv", "w", newline="",     encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Headline", "URL"])
            for headline, article_url in zip(headlines, links):  # Use zip to iterate over both lists
                csv_writer.writerow([headline, article_url])


            print("Headlines saved to CSV file.")

# Route to display the extracted headlines
@app.route("/")
def display_headlines():
    if not headlines:  # Ensure data is extracted first
        extract_data()

    html_output = ""
    zipped_data = list(zip(headlines, links))  # Create pairs of headlines and URLs

    return render_template("index.html", zipped_data=zipped_data)

if __name__ == "__main__":
    app.run(debug=True)