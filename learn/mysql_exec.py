# coding:UTF-8
import pymysql


if __name__ == '__main__':

    # 打开数据库连接
    db = pymysql.connect(host="localhost", port=3306, user="root", password="abc123", db="test", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    """
    【 创 建 表 】
    """
    # # 如果数据表已经存在使用 execute() 方法删除表。
    # cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    #
    # # 创建数据表SQL语句
    # sql = """CREATE TABLE EMPLOYEE (
    #          FIRST_NAME  CHAR(20) NOT NULL,
    #          LAST_NAME  CHAR(20),
    #          AGE INT,
    #          SEX CHAR(1),
    #          INCOME FLOAT )"""
    #
    # cursor.execute(sql)
    #
    # # 关闭数据库连接
    # db.close()


    """
    【 插 入 】
    """
    # # SQL 插入语句
    # sql = """INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME)
    #          VALUES ('zang', 'xin', 28, 'W', 7000)"""
    # try:
    #     # 执行sql语句
    #     cursor.execute(sql)
    #     # 提交到数据库执行
    #     db.commit()
    # except:
    #     # Rollback in case there is any error
    #     db.rollback()
    #
    # # 关闭数据库连接
    # db.close()


    """
    【 查 询 】
    """
    # SQL 查询语句
    sql = "SELECT * FROM EMPLOYEE WHERE INCOME > %s" % (1000)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取第一条记录
        # results = cursor.fetchone()
        # 获取2条记录
        results = cursor.fetchmany(size=2)
        # 获取所有记录列表
        # results = cursor.fetchall()
        for row in results:
            fname = row[0]
            lname = row[1]
            age = row[2]
            sex = row[3]
            income = row[4]
            # 打印结果
            print("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % (fname, lname, age, sex, income))
    except:
        print("Error: unable to fecth data")

    # 关闭数据库连接
    db.close()

    """
    【 更 新 】
    """
    # # SQL 更新语句
    # sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
    # try:
    #     # 执行SQL语句
    #     cursor.execute(sql)
    #     # 提交到数据库执行
    #     db.commit()
    # except:
    #     # 发生错误时回滚
    #     db.rollback()
    #
    # # 关闭数据库连接
    # db.close()

    """
    【 删 除 】
    """
    # # SQL 删除语句
    # sql = "DELETE FROM EMPLOYEE WHERE AGE > %s" % (20)
    # try:
    #     # 执行SQL语句
    #     cursor.execute(sql)
    #     # 提交修改
    #     db.commit()
    # except:
    #     # 发生错误时回滚
    #     db.rollback()
    #
    # # 关闭连接
    # db.close()