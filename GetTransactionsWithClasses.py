import os
import subprocess
import re
#import pandas as pd  ## accessed in Statement.py #dont need to keep using pandas, just insert the data as JSON. 
#import pyodbc  ##accessed in Statement.py
from Statement import Statement, Statementdetails


dir = r'C:\Users\chris\source\repos\StatementAnalysis'  #add this to config file to be more configurable. 

statementhist = r'C:\Users\chris\OneDrive\Desktop\Statement History\statementhist.txt'  #add this to config file to be more configurable.  ideally, this will be queried from the DB

StatementLog = r'C:\Users\chris\OneDrive\Desktop\Statement History\statementlog.txt'  #Still need to make this

##create separate class for regex -- does not need to be in this file. 
account = re.compile(r"(Account number:) (\d{4} \d{4} \d{4}).*") 
statementdate = re.compile(r"(for) [A-Z].*")

statement_hist = []

with open(statementhist, "r") as file:  #Change this to query, load keys from database into statementhist variable. 
    for line in file:
        statement_hist.append(line.splitlines())  #loads unique keys from txt file to list
        # print(line)

for filename in os.listdir(dir):
    if filename.endswith(".pdf") or filename.endswith(".pdf"):
        subprocess.run(['pdftotext', '-table', f"{filename}"], shell = True)  


                    
        
# Statements.gettextfile(Statements.directory)

for filename in Statement.directory:
        if filename.startswith('eStmt') and filename.endswith('.txt'):
            with open(filename, "r") as file:
                for line in file:
                    if account.search(line):
                            Statement.account_num = line[93:-1]
                            Statement.account_num = Statement.account_num.split()
                            Statement.account_num = ''.join(Statement.account_num)
                            Statement.account_num = re.sub('\D', '', Statement.account_num)
                            Statement.statement_id = Statement.account_num
                filename1 = str(filename)+str(Statement.account_num)  #This creates the key which will be used to determine if the specific file has already been inserted to SQL.
                
                if filename1 not in str(statement_hist):
                    #insert getdetails function here
                    Statementdetails.getdetails(filename)  #sql insert function (detailtosql()) is inside of getdetails method

                    with open(statementhist, "a") as file:
                        file.write(f"{filename1}\n") #Writes the key to file, which will be loaded into a list upon the code being run a second time. 
                        print(f"{filename1} was written to history and it's data was commited to the database")
            
            #possibly rename file to filename1 which is the unique key, but not sure if that would break something at this point        
                elif filename1 in str(statement_hist):
                    print(f"{filename1} already in database")
        






        

