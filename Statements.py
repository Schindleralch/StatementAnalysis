class Statements:  
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