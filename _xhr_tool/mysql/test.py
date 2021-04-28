import pymysql
# 初始化数据库连接
# 按实际情况依次填写MySQL的用户名、密码、IP地址、端口、数据库名

if __name__ == '__main__':
    # engine = create_engine('mysql+pymysql://root:12345678@localhost:3306/testdb')
    conn = pymysql.connect(host='localhost', user='root', password='512124632', database='crapydatabase')
    cur = conn.cursor()
    sql="select * from company"
    try:
        # 执行sql语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
    except:
    # Rollback in case there is any error
        conn.rollback()
    results = cur.fetchall()
    print(results)