# StatementAnalysis

This repository contains code that will take data from individual bank statements and insert that data into a local database for later consumption by a web API (tbd).  

# Dependencies 
- Chocolately package manager
	-to install Chocolatey visit the official Chocolatey documentation, or
		'''
		run powershell as administrator
		copy this powershell script: Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
		RUN
		'''
- PDFtoText (install from chocolately)
	- Open Powershell
	- run:
	'''
	choco install pdftotext
	'''