import peewee

db = peewee.MySQLDatabase('test2', user='root',
                          password='root', host='localhost', port=3306)



class basemodel(peewee.Model):
    class Meta:
        database = db

class userrec(basemodel):
    id = peewee.IntegerField(primary_key =True,unique=True)
    name = peewee.CharField(max_length=100)

db.connect()
# db.create_tables([userrec])

# userrec.create(id=1, name='firstperson')
# userrec.create(id=2, name='secondperson')

# q = userrec.select()
# for user in q:
#     print(user.id, user.name)

user = userrec.get(userrec.id == 2)
print(user.id, user.name)