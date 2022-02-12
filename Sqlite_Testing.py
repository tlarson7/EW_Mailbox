import sqlite3

cnxn = sqlite3.connect("EW_Review.db")
c = cnxn.cursor()
string = "9E5-Eagle"
# c.execute('INSERT INTO "Config_Info" VALUES ("18","a","b","c","d","e","f")')
# c.execute(f'SELECT * FROM "Config_Info" WHERE ? LIKE "%Config_Status%"',(string,))
c.execute('UPDATE Config_Info SET Company_Name = "ECorp" WHERE Config_Status = "Meow"')
# for row in c:
#     print(row)

cnxn.commit()
cnxn.close()