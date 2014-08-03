import os
from bs4 import BeautifulSoup
import Image
import cssutils

pathToStudents = os.path.join(".", "HTML Games")
studentNames = os.listdir(pathToStudents)
for studentName in studentNames:

    print "Student:", studentName
    
    pathToStudent = os.path.join(pathToStudents, studentName)
    filenames = os.listdir(pathToStudent)

    # Search the html files to find the images loaded through img or a tags
    imagesInGame = dict()
    for filename in filenames:
        
        if (filename.split(".")[-1] == "html") or (filename.split(".")[-1] == "htm"):
            filePath = os.path.join(pathToStudent, filename)

            print "\tParsing", filePath
    
            # Parse the HTML
            soup = BeautifulSoup(open(filePath))

            # Parse the CSS and build a dict of tags and widths
            cssDict = dict()
            cssString = ""
            for string in soup.head.style.strings: cssString += string
            sheet = cssutils.parseString(cssString)
            for rule in sheet:
                stringWidth = rule.style["width"]
                width = stringWidth.split("px")[0].strip()
                cssDict[rule.selectorText] = width 

            # Get all the images loaded through img tags
            imgTags = soup.findAll("img")
            for imgTag in imgTags:
                dKey = imgTag["src"].lower()
                imgID = "#"+imgTag["id"]

                # Figure out the width for the image
                width = 0
                
                # If this image has already been stored in the dict, imagesInGame,
                # then grab the stored image width
                if dKey in imagesInGame: width = imagesInGame[dKey]
                
                # Check if image is in the CSS for the current HTML file
                if imgID in cssDict:
                    cssWidth = eval(cssDict[imgID])
                    if cssWidth > width: width = cssWidth

                # Store the width in the dict, imagesInGame
                imagesInGame[dKey] = width                

            # Get all the images loaded through a tags
            aTags = soup.findAll("a")
            for aTag in aTags:
                extension = aTag["href"].split(".")[-1]
                if (extension == "jpg") or (extension == "jpeg") or (extension == "png"):  
                    dKey = aTag["href"].lower()
                    width = 800 # Default width
                    imagesInGame[dKey] = width

##    print "\tFiles used in game:"
##    for (size, imgName) in zip(imagesInGame.values(), imagesInGame.keys()):
##        print "\t\t",imgName
##        print "\t\t\tSize:", size 

    # Remove the images that aren't used
    # Resize the ones that are used
    print "\tFiles deleted:"
    for filename in filenames:
        filePath = os.path.join(pathToStudent, filename)
        extension = filename.split(".")[-1]
        if (extension == "psd"): os.remove(filePath)
        if (extension == "jpg") or (extension == "jpeg") or (extension == "png"):
            if not(filename.lower() in imagesInGame):
                os.remove(filePath)
                print "\t\t" + filePath
            else:
                # Resize
                im = Image.open(filePath)
                imWidth = im.size[0]
                newWidth = imagesInGame[filename.lower()]
                if (imWidth > newWidth):
                    print "\tResizing from", imWidth, "to", newWidth
                    im.thumbnail([newWidth, newWidth], Image.ANTIALIAS)
                    im.save(filePath, "JPEG")

    print

