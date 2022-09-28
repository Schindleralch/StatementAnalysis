import pyodbc

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