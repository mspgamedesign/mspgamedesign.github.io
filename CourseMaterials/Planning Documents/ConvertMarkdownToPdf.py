# Convert markdown files to printable PDFs using the command line tool, Pandoc
#	Requires: Pandoc, http://johnmacfarlane.net/pandoc/installing.html

import subprocess
import os

filesInCurrentDirectory = os.listdir(os.getcwd())
for filename in filesInCurrentDirectory:
	name, extension = filename.split(".")
	outputFilename = name + ".pdf"

	if extension == "md":
		subprocess.call(["pandoc", filename,
						"-V", "geometry:margin=1in",
						"-o", outputFilename])

