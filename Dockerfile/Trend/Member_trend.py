import datetime

import pymysql.cursors
import os

host = os.environ['MARIADB_IP']
user = os.environ['MARIADB_USER']
password = os.environ['MARIADB_PASSWORD']
db = os.environ['MARIADB_DATABASE']


def makeTrendTable():
    # Create trend table if not exist
    make_trend_tabel_sql = "CREATE TABLE IF NOT EXISTS trend (_ID int NOT NULL AUTO_INCREMENT, PRIMARY KEY (_ID) , avg_price int(11), quantity int(11), stock_code varchar(255), stock_name varchar(255), member_id bigint(20), date DATE )"
    cur.execute(make_trend_tabel_sql)
    conn.commit()

def insertTrend():
    # 메인 코드
    select_all_stock_sql = "SELECT * FROM ka.stock"
    cur.execute(select_all_stock_sql)
    conn.commit()
    values = []
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # # for dummny
    # d1today = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    # d2today = (datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%d")

    for i in cur.fetchall():
        values.append(
            (str(i['avg_price']), str(i['quantity']), i['stock_code'], i['stock_name'], str(i['member_id']), str(today)))

        # # for dummy
        # values.append(
        #     (str(i['avg_price']*10), str(i['quantity']+10), i['stock_code'], i['stock_name'], str(i['member_id']), str(d1today)))
        # values.append(
        #     (str(i['avg_price']*100), str(i['quantity']+20), i['stock_code'], i['stock_name'], str(i['member_id']), str(d2today)))

    insert_trend_sql = "INSERT INTO `ka`.`trend` (`avg_price`, `quantity`, `stock_code`, `stock_name`, `member_id`, `date`) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.executemany(insert_trend_sql, values)
    conn.commit()

if __name__ == "__main__":
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(today)

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')  # 접속정보
    cur = conn.cursor(pymysql.cursors.DictCursor)  # 커서생성

    makeTrendTable()
    insertTrend()

    conn.close()	# 종료