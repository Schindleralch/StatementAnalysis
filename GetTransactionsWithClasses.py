import collections
import os
import subprocess
import re
import pandas as pd  #dont need to keep using pandas, just insert the data as JSON. 
import pyodbc
import datetime
import time

#Still need to add StatementLog file to print to a text file the files that were attempted to be committed and print the dataframe to it. Use Time or Datetime for this

dir = r'C:\Users\chris\source\repos\StatementAnalysis'  #add this to config file to be more configurable. 

statementhist = r'C:\Users\chris\OneDrive\Desktop\Statement History\statementhist.txt'  #add this to config file to be more configurable.  ideally, this will be queried from the DB

StatementLog = r'C:\Users\chris\OneDrive\Desktop\Statement History\statementlog.txt'  #Still need to make this

##create separate class for regex -- does not need to be in this file. 
account = re.compile(r"(Account number:) (\d{4} \d{4} \d{4}).*") 
statementdate = re.compile(r"(for) [A-Z].*")
detail = re.compile(r'(\d{2}[/.-]\d{2}[/.-]\d{2})(.*)')
statement_hist = []

with open(statementhist, "r") as file:  #Change this to query, load keys from database into statementhist variable. 
    for line in file:
        statement_hist.append(line.splitlines())  #loads unique keys from txt file to list
        # print(line)

for filename in os.listdir(dir):
    if filename.endswith(".pdf") or filename.endswith(".pdf"):
        subprocess.run(['pdftotext', '-table', f"{filename}"], shell = True)  


class Statements:  #add to separate file, import into this one. 
    # statementhist = r'C:\Users\chris\OneDrive\Desktop\Statement History\statementhist.txt'
    global dir
    directory = os.listdir(r'c:\Users\chris\OneDrive\Desktop\Pythoncodes\Bank Account Project')  
    def __init__(self, account_num, statement_date, statement_id):  #Statement_id is the statement date + accountnumber. 
        self.account_num = account_num
        self.statement_date = statement_date
        self.statement_id = statement_id
        

    def gettextfile(self):
        for x in Statements.directory:
            Statements.filename = x
            if x.endswith(".pdf") or x.endswith(".pdf"):
                subprocess.run(['pdftotext', '-table', f"{x}"], shell = True)
                # print(x)
                



class Statementdetails(Statements):
    def __init__(self, trans_date, trans_desc, trans_amount, account_num):
        super().__init__(account_num)
        self.trans_date = trans_date
        self.trans_desc = trans_desc
        self.trans_amount = trans_amount

    def getdetails(self):
        with open(filename, "r") as file:
            for line in file:
                if detail.match(line):
                    line = line.split()
                    date, *desc = line
                    # Statementdetails(trans_date= date, trans_desc= ' '.join(line[1:-1]), trans_amount= line[-1], account_num= Statements.account_num) #this don't work
                    Statementdetails.trans_desc = ' '.join(line[1:-1])
                    Statementdetails.trans_amount = line[-1]
                    Statementdetails.trans_date = date
                    #print(f"{type(Statementdetails.trans_date)} {type(Statementdetails.trans_desc)} {type(Statementdetails.trans_amount)} {type(Statements.account_num[-4:])}")
                    
                    try:
                        global dfdict
                        dfdict = {
                            "trans_date" : [Statementdetails.trans_date],
                            "trans_desc" : [Statementdetails.trans_desc],
                            "trans_amount" : [Statementdetails.trans_amount],
                            "account_id" : [Statements.account_num[-4:]]
                        }
                        df = pd.DataFrame(dfdict)
                        df['trans_date'] = pd.to_datetime(df['trans_date'])
                        # df['account_id'] = pd.to_numeric(df['account_id'])
                        df['trans_amount'] = df['trans_amount'].map(lambda x: float(x.replace(',', '')))
                        df['trans_desc'] = df['trans_desc'].astype(str)

                        # print(df)

                    except ValueError: 
                        print(ValueError)
                    # detailtoSql()
                    try:
                        detailtoSql(df)
                    except pyodbc.ProgrammingError:
                        print(Exception)
            # try:
            #     dfdict['account_id'].append(f"{Statementdetails.account_num[-4:]}") #try appending all values to large dataframe instead of inserting after creating one row
            # except:
            #     Exception


                    
class Sql:
    pass                
def detailtoSql(df): 
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost\SQLEXPRESS;'
                      'Database=StatementAnalysis;'
                      'Trusted_Connection=yes;')

    cursor = conn.cursor()
    # query = (f"INSERT INTO dbo.transactions (trans_date, trans_description, trans_amount, account_id) VALUES(?,?,?,?)")
    for index, row in df.iterrows():
        query = (f"INSERT INTO dbo.Transactions (trans_date, trans_description, trans_amount, account_id) VALUES(?,?,?,?)") 
        cursor.execute(query, row.trans_date, row.trans_desc, row.trans_amount, row.account_id )
    conn.commit()
    cursor.close()
    print(f"inserted: {df}")
        

class Vendor(Statements):
    def __init__(self, vendorname):
        self.name = vendorname



# Statements.gettextfile(Statements.directory)

for filename in Statements.directory:
        if filename.startswith('eStmt') and filename.endswith('.txt'):
            with open(filename, "r") as file:
                for line in file:
                    if account.search(line):
                            Statements.account_num = line[93:-1]
                            Statements.account_num = Statements.account_num.split()
                            Statements.account_num = ''.join(Statements.account_num)
                            Statements.account_num = re.sub('\D', '', Statements.account_num)
                            Statements.statement_id = Statements.account_num
                filename1 = str(filename)+str(Statements.account_num)  #This creates the key which will be used to determine if the specific file has already been inserted to SQL.
                
                if filename1 not in str(statement_hist):
                    #insert getdetails function here
                    Statementdetails.getdetails(filename)  #sql insert function (detailtosql()) is inside of getdetails method

                    with open(statementhist, "a") as file:
                        file.write(f"{filename1}\n") #Writes the key to file, which will be loaded into a list upon the code being run a second time. 
                        print(f"{filename1} was written to history and it's data was commited to the database")
            
            #possibly rename file to filename1 which is the unique key, but not sure if that would break something at this point        
                elif filename1 in str(statement_hist):
                    print(f"{filename1} already in database")
        

try:
    print(dfdict)
except:
    if Exception:
        Exception
        print("No Data Loaded")





        

