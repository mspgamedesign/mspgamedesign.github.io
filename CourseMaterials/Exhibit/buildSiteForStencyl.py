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
pathToGameDirectory = os.path.join(os.getcwd(), "Stencyl")
pathToStudentGames = os.path.join(pathToGameDirectory, "Stencyl Games")
pathToSiteTemplates = os.path.join(pathToGameDirectory, "HTML Templates")
pathToIndexTemplate = os.path.join(pathToSiteTemplates, "indexTemplate.html")
pathToGameTemplate = os.path.join(pathToSiteTemplates, "gameTemplate.html")
pathToIndexOfSite = os.path.join(pathToGameDirectory, "index.html")

# Remove the last generated version of the site
removeGeneratedSite(pathToGameDirectory)

# Load in the HTML template for table of contents page
with open(pathToIndexTemplate, "r") as fh:
    soup = BeautifulSoup(fh)
    
# Each directory within pathToStudentGames contains a student's game
directoryNames = os.listdir(pathToStudentGames)

# Load student names
dAliases = loadStudentNamesAndAliases()

for directoryName in directoryNames:
    pathToStudentDirectory = os.path.join(pathToStudentGames, directoryName) 
    if os.path.isdir(pathToStudentDirectory):
        
        # We found a student's game
        anonName = directoryName
        realName, alias = dAliases[anonName]
        pathToGamePage = anonName+".html" # Page containing swf of Stencyl game

        # Files in .\Stencyl Games\Student Name\
        # Time to find the .swf file
        filenames = os.listdir(pathToStudentDirectory)
        for filename in filenames:
            extension = filename.split(".")[-1]
            if extension == "swf": break
        if filename[-4:] != ".swf": print "ERROR: No SWF found"
        pathToSWF = os.path.join("Stencyl Games", anonName, filename)

        # Insert a hyperlinked paragraph into the main section of the index HTML
        paragraph = soup.new_tag("p")
        paragraph["class"] = "centeredtext"
        hyperlink = soup.new_tag("a", href=pathToGamePage)
        hyperlink.string = alias
        paragraph.insert(0, hyperlink)
        soup.section.append(paragraph)

        # Create a game page for the student game
        # Get resolution
        pathToResolution = os.path.join(pathToStudentDirectory, "resolution.txt")
        width = "0"
        height = "0"
        with open(pathToResolution, "r") as fh:
            width, height = fh.readline().strip().split(",")
        
        with open(pathToGameTemplate, "r") as fh:
            gamePageSoup = BeautifulSoup(fh)

            # Add a title with the students name
            titleTag = gamePageSoup.new_tag("title")
            titleTag.string = alias
            gamePageSoup.head.append(titleTag)

            gamePageSoup.body.div["style"] = "width:"+width+"px;height:"+height+"px;margin:0 auto;"
            
            # Add the stencyl swf to the div with class gamecontainer
            swfTag = gamePageSoup.new_tag("object", data=pathToSWF)
            swfTag["class"] = "game"
            gamePageSoup.body.div.append(swfTag)
    
            # Save the student's game page
            with open(os.path.join(pathToGameDirectory, pathToGamePage), "w") as outFile:
                outFile.write(gamePageSoup.prettify("utf-8"))
            
# Save the main page
with open(pathToIndexOfSite, "w") as fh:
    fh.write(soup.prettify("utf-8"))
    

