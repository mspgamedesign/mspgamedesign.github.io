# Code used to change the files from student names to anon names
import os
import subprocess

def renameDirectories(pathToStudentGames, dNames):
	studentDirectories = os.listdir(pathToStudentGames)
	for directory in studentDirectories:
		if directory in dNames:
			anonName = dNames[directory]
			pathToDirectory = os.path.join(pathToStudentGames, directory)
			pathToNewDirectory = os.path.join(pathToStudentGames, anonName)
			print "Renaming..."
			print "\t" + pathToDirectory
			print "\t" + pathToNewDirectory
			os.rename(pathToDirectory, pathToNewDirectory)

originalPath = os.getcwd()
pathToHTMLGames = os.path.join(originalPath, "HTML") 
pathToJSGames = os.path.join(originalPath, "JavaScript") 
pathToStencylGames = os.path.join(originalPath, "Stencyl")

# Names and associated aliases are stored in a text file where each line is:
# 	Anonymous Name, Student Name, Alias
dAliases = dict()
dNames = dict()
with open("Student Names and Aliases.txt") as fh:
	fh.readline() # Disregard the header
	for line in fh:
		anonName, realName, alias = [i.strip() for i in line.split(",")]
		dAliases[anonName] = (realName, alias)
		dNames[realName] = anonName

renameDirectories(os.path.join(pathToHTMLGames, "HTML Games"), dNames)
renameDirectories(os.path.join(pathToJSGames, "Modified JavaScript Games"), dNames)
renameDirectories(os.path.join(pathToStencylGames, "Stencyl Games"), dNames)
renameDirectories(os.path.join(os.getcwd(), "Original Game Backups", "HTML Games"), dNames)
