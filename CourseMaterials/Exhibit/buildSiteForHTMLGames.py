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
pathToGameDirectory = os.path.join(os.getcwd(), "HTML")
pathToStudentGames = os.path.join(pathToGameDirectory, "HTML Games")
pathToSiteTemplates = os.path.join(pathToGameDirectory, "HTML Templates")
pathToIndexTemplate = os.path.join(pathToSiteTemplates, "indexTemplate.html")
pathToGameTemplate = os.path.join(pathToSiteTemplates, "gameTemplate.html")
pathToIndexOfSite = os.path.join(pathToGameDirectory, "index.html")

# Remove the last generated version of the site
removeGeneratedSite(pathToGameDirectory)

# Each directory is a students game
directoryNames = os.listdir(pathToStudentGames)

# Load in the HTML template
with open(pathToIndexTemplate, "r") as fh: 
    soup = BeautifulSoup(fh)

# Load student names
dAliases = loadStudentNamesAndAliases()

for directoryName in directoryNames:
    pathToStudentDirectory = os.path.join(pathToStudentGames, directoryName) 
    if os.path.isdir(pathToStudentDirectory):

        # We found a student's game
        anonName = directoryName
        realName, alias = dAliases[anonName]
        pathToOldGamePage = os.path.join(pathToStudentDirectory, "index.html") # This is the index file within each student's directory
        pathToNewGamePage = os.path.join(pathToGameDirectory, anonName+".html") # This is the iframe game page we create below

        # Insert a hyperlinked paragraph into the main section of the index HTML
        paragraph = soup.new_tag("p")
        paragraph["class"] = "centeredtext"
        hyperlink = soup.new_tag("a", href=anonName+".html")
        hyperlink.string = alias
        paragraph.insert(0, hyperlink)
        soup.section.append(paragraph)

        # Create a game page for the student game
        with open(pathToGameTemplate, "r") as fh:
            gamePageSoup = BeautifulSoup(fh)

            # Add a title with the students name
            titleTag = gamePageSoup.new_tag("title")
            titleTag.string = alias
            gamePageSoup.head.insert(0, titleTag)

            # Add an iframe that loads the student game
            iframeTag = gamePageSoup.new_tag("iframe", src=os.path.join("HTML Games", anonName, "index.html"))
            gamePageSoup.body.append(iframeTag)

            # Save the student's game page
            with open(pathToNewGamePage, "w") as outFile:
                outFile.write(gamePageSoup.prettify("utf-8"))
            
# Save the main page
with open(pathToIndexOfSite, "w") as fh:
    fh.write(soup.prettify("utf-8"))