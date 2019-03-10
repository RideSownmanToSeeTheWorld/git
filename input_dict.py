import pymysql
f = open ("/home/tarena/aid/inter/day10/dictionary/dict.txt")

db = pymysql.connect('localhost','root','123456','Dictionary')

cursor = db.cursor()
for line in f:
    tmp = line.split(' ')
    word = tmp[0]
    mean = ' '.join(tmp[1:]).strip()
    sql = 'insert into words (word, mean) values ("%s","%s")'%(word,mean)
    try:
        cursor.execute(sql)
        db.commit() #提交到数据库执行，一定要记提交哦  
    except:
        db.rollback() #发生错误时回滚
f.close()


