import os
from bs4 import BeautifulSoup

# Path to HTML games
pathToStudentGames = os.path.join(".", "HTML Games")
# Each directory is a students game
directoryNames = os.listdir(pathToStudentGames)

# Load in the HTML template
pathToIndexTemplate = os.path.join(".", "HTML Templates", "indexTemplate.html")
with open(pathToIndexTemplate, "r") as fh:
    soup = BeautifulSoup(fh)


for directoryName in directoryNames:

    pathToStudentDirectory = os.path.join(pathToStudentGames, directoryName) 

    if os.path.isdir(pathToStudentDirectory):
        # We found a student's game
        studentName = directoryName
        pathToOldGamePage = os.path.join(pathToStudentDirectory, "index.html") # This is the index file within each student's directory
        pathToNewGamePage = studentName + ".html" # This is the iframe game page we create below


        # Insert a hyperlinked paragraph into the main section of the index HTML
        paragraph = soup.new_tag("p")
        paragraph["class"] = "centeredtext"
        hyperlink = soup.new_tag("a", href=pathToNewGamePage)
        hyperlink.string = studentName
        paragraph.insert(0, hyperlink)
        soup.section.append(paragraph)

        # Create a game page for the student game
        pathToGameTemplate = os.path.join(".", "HTML Templates", "gameTemplate.html")
        with open(pathToGameTemplate, "r") as fh:
            gamePageSoup = BeautifulSoup(fh)

            # Add a title with the students name
            titleTag = gamePageSoup.new_tag("title")
            titleTag.string = studentName
            gamePageSoup.head.insert(0, titleTag)

            # Add an iframe that loads the student game
            iframeTag = gamePageSoup.new_tag("iframe", src=pathToOldGamePage)
            gamePageSoup.body.append(iframeTag)

            # Save the student's game page
            with open(pathToNewGamePage, "w") as outFile:
                outFile.write(gamePageSoup.prettify("utf-8"))
            
# Save the main page
with open("index.html", "w") as fh:
    fh.write(soup.prettify("utf-8"))
    

