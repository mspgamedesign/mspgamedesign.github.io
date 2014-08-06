import os 

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

# Path to the page we are going to make
pathToStencylPage = os.path.join("..", "stencyl", "index.html")

# Get a list of the students who made games
pathToStencylGames = os.path.join("..", "games", "Stencyl")
studentGameDirectories = os.listdir(pathToStencylGames) 

# Load student names
dAliases = loadStudentNamesAndAliases()

with open(pathToStencylPage, "w") as fh:
	fh.write("---\n")
	fh.write("layout: page\n")
	fh.write("title: Platformer Game\n")
	fh.write("---\n")
	fh.write("words words words\n\n")

	numGames = len(studentGameDirectories)
	gamesPerRow = 3
	for i in range(0, numGames, 3):
		fh.write("\n<div class='row'>\n")
		for di in range(0, gamesPerRow, 1):
			if i+di >= numGames: break

			studentGameDirectory = studentGameDirectories[i+di]
			pathToInfo = os.path.join("..", "games", "Stencyl", studentGameDirectory, "Game Info.txt")
			with open(pathToInfo, "r") as gameInfoFile:
				title = gameInfoFile.readline().split(":")[-1].strip()
			gameTitle = title
			
			realName, alias = dAliases[studentGameDirectory]

			screenshotURL = "../games/Stencyl/{0}/{1}.png".format(studentGameDirectory, gameTitle)
			postURL = "../2014/08/04/{0}_Stencyl.html".format(alias)
			 


			fh.write("\t<a href='{0}'>\n".format(postURL))
			fh.write("\t\t<figure class='grid-third'>\n")
			fh.write("\t\t\t<img src='{0}'>\n".format(screenshotURL))
			fh.write("\t\t\t<figcaption>{0}</figcaption>\n".format(alias))
			fh.write("\t\t</figure>\n")
			fh.write("\t</a>\n")
		fh.write("</div>\n")
