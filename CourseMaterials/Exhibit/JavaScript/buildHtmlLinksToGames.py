import os
from bs4 import BeautifulSoup

# Path to JS games
pathToOriginalStudentGames = os.path.join(".", "Original JavaScript Games")
pathToModifiedStudentGames = os.path.join(".", "Modified JavaScript Games")

# Each directory is a students game
directoryNames = os.listdir(pathToOriginalStudentGames)

# Load in the HTML template
pathToIndexTemplate = os.path.join(".", "HTML Templates", "indexTemplate.html")
with open(pathToIndexTemplate, "r") as fh:
    soup = BeautifulSoup(fh)

for directoryName in directoryNames:

    pathToStudentDirectory = os.path.join(pathToOriginalStudentGames, directoryName) 

    if os.path.isdir(pathToStudentDirectory):
        # We found a student's game
        studentName = directoryName
        pathToOldGamePage = os.path.join(pathToOriginalStudentGames, studentName, "index.html") # This is the index file within each student's directory
        pathToNewGamePage = os.path.join(pathToModifiedStudentGames, studentName, "index.html") # This is the iframe game page we create below

        # Insert a hyperlinked paragraph into the main section of the index HTML
        paragraph = soup.new_tag("p")
        paragraph["class"] = "centeredtext"
        hyperlink = soup.new_tag("a", href=pathToNewGamePage)
        hyperlink.string = studentName
        paragraph.insert(0, hyperlink)
        soup.section.append(paragraph)

        # Modify the JS so that the script is inside the body
        #   This way, when the JS loads after the DOM, so that it will
        #   switch pages away from the game list to the individual page before
        #   the first alert
        with open(pathToOldGamePage, "r") as fh:
            gamePageSoup = BeautifulSoup(fh)
            script = gamePageSoup.head.script.extract()
            gamePageSoup.body.append(script)
            
            # Add a title with the students name
            titleTag = gamePageSoup.new_tag("title")
            titleTag.string = studentName
            gamePageSoup.head.append(titleTag)

            # Link to get back to the list of games
            paragraph = soup.new_tag("p")
            hyperlink = soup.new_tag("a", href="../../index.html")
            hyperlink.string = "Back to Games List"
            paragraph.insert(0, hyperlink)
            gamePageSoup.body.append(paragraph)

            
            # Save the modified JS
            with open(pathToNewGamePage, "w") as outFile:
                outFile.write(gamePageSoup.prettify("utf-8"))

        
##        # Create a game page for the student game
##        pathToGameTemplate = os.path.join(".", "HTML Templates", "gameTemplate.html")
##        with open(pathToGameTemplate, "r") as fh:
##            gamePageSoup = BeautifulSoup(fh)
##
##
##            
##            # Add an iframe that loads the student game
##            iframeTag = gamePageSoup.new_tag("iframe", src=pathToNewGamePage)
##            gamePageSoup.body.append(iframeTag)
##
##            # Save the student's game page
##            with open(studentName+".html", "w") as outFile:
##                outFile.write(gamePageSoup.prettify("utf-8"))



        
            
# Save the main page
with open("index.html", "w") as fh:
    fh.write(soup.prettify("utf-8"))
    

