import redis
import sqlite3

conn = sqlite3.connect('test.db')

cursor = conn.cursor()
try:
    cursor.execute("""create table user1(id int, name varchar(20), age int);""")
except sqlite3.OperationalError as e:
    print(str(e))
cursor.execute("""insert into user1 values(0, 'xiaoming', 10);""")
conn.commit()

cursor.execute("""select name, age from user1;""")
values = cursor.fetchall()
for value in values:
    print(value)


r = redis.Redis()

print(r.get('test'))

def cache_aside():
    age = r.get('xiaoming')
    if age:
        return age
    else:
        values = conn.execute("""select name, age from user1;""")
        for name, age in values:
            if name == 'xiaoming':
                r.set('xiaoming', age)
                r.expire('xiaoming', 5)
                return age
    return None

s = cache_aside()
print(r.get('xiaoming'))
print(s)


conn.close()