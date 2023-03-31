import requests
from bs4 import BeautifulSoup
import csv

print("Script is running...")

# URL of the Oxford Learner's Dictionary
base_url = "https://www.oxfordlearnersdictionaries.com"

# Make a GET request to the URL and parse the HTML content using BeautifulSoup
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
response = requests.get(base_url + "/wordlists/oxford3000-5000", headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find all the li elements under ul element with class="top-g"
li_elements = soup.find("ul", class_="top-g").find_all("li")

# Create an empty list to store the word objects
words_list = []

# Loop through each li element and extract the word, pronunciation, and link
for li in li_elements:
    word = li.a.text.strip()
    
    word_type = li.span.text.strip()
    word_url = li.a["href"]
    link = f'<a href={base_url + word_url}>{word_type}</a>'
    
    pronunciation_container = li.find("div", class_="sound audio_play_button icon-audio pron-us")
    pronunciation_url = "" if pronunciation_container is None else pronunciation_container["data-src-mp3"]
    pronunciation = f'<audio controls><source src={base_url + pronunciation_url} type="audio/mp3"></audio>'

    word_object = {"word": word,"pronunciation": pronunciation, "link": link}
    words_list.append(word_object)
    if len(words_list) >= 5000:
        break

# Print the list of word objects
# print(words_list)

# Define the field names for the CSV file
field_names = ["word", "pronunciation", "link"]

# Open a new CSV file for writing
with open("words.csv", "w", newline="") as csvfile:
    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=field_names)

    # Write the header row to the CSV file
    writer.writeheader()

    # Write each word to the CSV file
    for word in words_list:
        writer.writerow(word)

print("Script is done!")