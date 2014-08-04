import os
from bs4 import BeautifulSoup


def loadStudentNamesAndAliases():
    # Load in student names and their aliases
    #   Names and associated aliases are stored in a text file where each line is:
    #       Anonymous Name, Student Name, Alias
    dAliases = dict()
    with open("Student Names and Aliases.txt") as fh:
        fh.readline() # Disregard the header
        for line in fh:
            anonName, realName, alias = [i.strip() for i in line.split(",")]
            dAliases[anonName] = (realName, alias)
    return dAliases

def removeGeneratedSite(path):
    filenames = os.listdir(path)
    for filename in filenames:
        extension = filename.split(".")[-1].lower()
        if extension == "html":
            os.remove(os.path.join(path, filename))


# Set up a bunch of the path information upfront
pathToGameDirectory = os.path.join(os.getcwd(), "JavaScript")
pathToOriginalStudentGames = os.path.join(os.getcwd(), "Original Game Backups", "Original JavaScript Games")
pathToModifiedStudentGames = os.path.join(pathToGameDirectory, "Modified JavaScript Games")
pathToSiteTemplates = os.path.join(pathToGameDirectory, "HTML Templates")
pathToIndexTemplate = os.path.join(pathToSiteTemplates, "indexTemplate.html")
pathToGameTemplate = os.path.join(pathToSiteTemplates, "gameTemplate.html")
pathToIndexOfSite = os.path.join(pathToGameDirectory, "index.html")

# Each directory is a students game
directoryNames = os.listdir(pathToOriginalStudentGames)

# Remove the last generated version of the site
removeGeneratedSite(pathToGameDirectory)

# Load in the HTML template
with open(pathToIndexTemplate, "r") as fh:
    soup = BeautifulSoup(fh)

# Load student names
dAliases = loadStudentNamesAndAliases()

for directoryName in directoryNames:
    pathToStudentDirectory = os.path.join(pathToOriginalStudentGames, directoryName) 
    if os.path.isdir(pathToStudentDirectory):

        # We found a student's game
        anonName = directoryName
        realName, alias = dAliases[anonName]
        pathToOldGamePage = os.path.join(pathToOriginalStudentGames, anonName, "index.html") # This is the index file within each student's directory
        pathToNewGamePage = os.path.join(pathToModifiedStudentGames, anonName, "index.html") # This is the iframe game page we create below

        # Insert a hyperlinked paragraph into the main section of the index HTML
        paragraph = soup.new_tag("p")
        paragraph["class"] = "centeredtext"
        hyperlink = soup.new_tag("a", href=os.path.join("Modified JavaScript Games", anonName, "index.html"))
        hyperlink.string = alias
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
            titleTag.string = alias
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
            
# Save the main page
with open(pathToIndexOfSite, "w") as fh:
    fh.write(soup.prettify("utf-8"))
    







##        # Create a game page for the student game
##        pathToGameTemplate = os.path.join(".", "HTML Templates", "gameTemplate.html")
##        with open(pathToGameTemplate, "r") as fh:
##            gamePageSoup = BeautifulSoup(fh)
##            
##            # Add an iframe that loads the student game
##            iframeTag = gamePageSoup.new_tag("iframe", src=pathToNewGamePage)
##            gamePageSoup.body.append(iframeTag)
##
##            # Save the student's game page
##            with open(studentName+".html", "w") as outFile:
##                outFile.write(gamePageSoup.prettify("utf-8"))


