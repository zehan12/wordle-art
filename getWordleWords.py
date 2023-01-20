"""Get list of Wordle words.
"""

from datetime import datetime

from bs4 import BeautifulSoup
import requests

WORDLE_URL = "https://www.nytimes.com/games/wordle/"
FILENAME = f"wordle-words-{datetime.today().strftime('%Y-%m-%d')}.txt"


def main():
    """Get the current Wordle word list and write it to a text file."""

    # Get the source of the Wordle homepage and parse with BeautifulSoup.
    response = requests.get(WORDLE_URL + "index.html")
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the name of the script file that contains the word list.
    scripts = [script.attrs.get("src") for script in soup.select("script[src]")]
    script_filename = ""
    for script in scripts:
        if script.startswith("main."):
            script_filename = script
            exit
    if not script_filename:
        print(
            "main.???.js script file! Try again, this seems to happen intermittently."
        )
        return

    # Get the text of the script file and extract the word list (which is a list
    # assigned to the variable ko).
    response = requests.get(WORDLE_URL + script_filename)
    for line in response.text.split(";"):
        if line.startswith("var ko=["):
            start = line.find("[")
            end = line.find("]")
            wordlist_text = line[start + 1 : end]
            words = [word for word in wordlist_text.split(",")]
            wordlist = [word[1:-1] for word in words]

    # Write the word list to a text file.
    with open(FILENAME, "w", encoding="utf-8", newline="\n") as fhandle:
        for word in wordlist:
            fhandle.write(f"{word}\n")
    print(f"Current list of {len(wordlist)} words written to {FILENAME}")


if __name__ == "__main__":
    main()
