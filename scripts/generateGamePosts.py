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


# Load student names
dAliases = loadStudentNamesAndAliases()


# Path to where the posts should be put
pathToPosts = os.path.join("..", "_posts")


for anonName in dAliases:
	realName, alias = dAliases[anonName]

	# HTML Game Post (if it exists)
	pathToStudentDir = os.path.join("..", "games", "HTML", anonName)
	if os.path.exists(pathToStudentDir):
		pathToPost = os.path.join(pathToPosts, "2014-08-04-"+alias+"_HTML.html")
		with open(pathToPost, "w") as fh:
			# yaml front matter
			fh.write("---\n")
			fh.write("layout: htmlGame\n")
			fh.write("title: "+alias+"\n")
			fh.write("tags: HTML5\n")
			fh.write("---\n")

			# yaml content
			fh.write("<iframe src='../../../games/HTML/"+anonName+"/index.html'></iframe>")


	# JavaScript Game Post (if it exists)
	pathToStudentDir = os.path.join("..", "games", "JavaScript", anonName)
	if os.path.exists(pathToStudentDir):
		pathToPost = os.path.join(pathToPosts, "2014-08-04-"+alias+"_JavaScript.html")
		pathToJSGame = os.path.join("..", "games", "JavaScript", anonName, "index.html")
		soup = BeautifulSoup(open(pathToJSGame))
		scriptString = str(soup.body.script)
		with open(pathToPost, "w") as fh:
			# yaml front matter
			fh.write("---\n")
			fh.write("layout: javascriptGame\n")
			fh.write("title: "+alias+"\n")
			fh.write("tags: JavaScript\n")
			fh.write("---\n")

			# yaml content
			fh.write(scriptString)

	# Stencyl Game Post (if it exists)
	pathToStudentDir = os.path.join("..", "games", "stencyl", anonName)
	if os.path.exists(pathToStudentDir):
		pathToPost = os.path.join(pathToPosts, "2014-08-04-"+alias+"_Stencyl.html")

		# Get game resolution and filename
		pathToResolution = os.path.join(pathToStudentDir, "Game Info.txt")
		width, height = "0", "0"
		with open(pathToResolution, "r") as fh:
			title = fh.readline().split(":")[-1].strip()
			width, height = fh.readline().split(":")[-1].split(",")
			width, height = width.strip(), height.strip()
		swfFilename = title+".swf"

		with open(pathToPost, "w") as fh:
			# yaml front matter
			fh.write("---\n")
			fh.write("layout: stencylGame\n")
			fh.write("title: "+alias+"\n")
			fh.write("tags: stencyl\n")
			fh.write("---\n")

			# yaml content
			fh.write("<section style='width:{0}px;height:{1}px;margin:0 auto;'>".format(width, height))
			fh.write("<object class='game' data='../../../games/Stencyl/{0}/{1}' style='width:{2}px; height:{3}px'>".format(anonName, swfFilename, width, height))
			fh.write("</object>")
			fh.write("</section>")