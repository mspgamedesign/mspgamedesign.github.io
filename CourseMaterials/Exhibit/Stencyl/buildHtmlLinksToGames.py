import os
from bs4 import BeautifulSoup

# Load in the HTML template for table of contents page
pathToIndexTemplate = os.path.join(".", "HTML Templates", "indexTemplate.html")
with open(pathToIndexTemplate, "r") as fh:
    soup = BeautifulSoup(fh)
    
# Path to Stencyl games
pathToStudentGames = os.path.join(".", "Stencyl Games")

# Each directory within pathToStudentGames contains a student's game
directoryNames = os.listdir(pathToStudentGames)

for directoryName in directoryNames:

    pathToStudentDirectory = os.path.join(pathToStudentGames, directoryName) 
    if os.path.isdir(pathToStudentDirectory):
        
        # We found a student's game
        studentName = directoryName
        pathToGamePage = studentName+".html" # Page containing swf of Stencyl game

        # Files in .\Stencyl Games\Student Name\
        # Time to find the .swf file
        filenames = os.listdir(pathToStudentDirectory)
        for filename in filenames:
            extension = filename.split(".")[-1]
            if extension == "swf":
                break
        if filename[-4:] != ".swf": print "ERROR: No SWF found"
        pathToSWF = os.path.join(pathToStudentDirectory, filename)

        # Insert a hyperlinked paragraph into the main section of the index HTML
        paragraph = soup.new_tag("p")
        paragraph["class"] = "centeredtext"
        hyperlink = soup.new_tag("a", href=pathToGamePage)
        hyperlink.string = studentName
        paragraph.insert(0, hyperlink)
        soup.section.append(paragraph)

        # Create a game page for the student game
        pathToGameTemplate = os.path.join(".", "HTML Templates", "gameTemplate.html")
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
            titleTag.string = studentName
            gamePageSoup.head.append(titleTag)

            gamePageSoup.body.div["style"] = "width:"+width+"px;height:"+height+"px;margin:0 auto;"
            
            # Add the stencyl swf to the div with class gamecontainer
            swfTag = gamePageSoup.new_tag("object", data=pathToSWF)
            swfTag["class"] = "game"
            gamePageSoup.body.div.append(swfTag)
    
            # Save the student's game page
            with open(pathToGamePage, "w") as outFile:
                outFile.write(gamePageSoup.prettify("utf-8"))



        
            
# Save the main page
with open("index.html", "w") as fh:
    fh.write(soup.prettify("utf-8"))
    

