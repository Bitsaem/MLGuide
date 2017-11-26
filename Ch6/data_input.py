import pymysql

conn = pymysql.connect ( host = 'localhost', user = 'surf', password = 'stormsex'
                         ,db = 'findb', charset = 'utf8')
sql = " select * from stock_price where stock_price.code = '005930'"
curs = conn.cursor()

rows = curs.execute(sql)

