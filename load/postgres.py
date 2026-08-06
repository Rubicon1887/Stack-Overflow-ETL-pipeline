import psycopg

cnxn=psycopg.connect(
    host='localhost',
    dbname='stkof',
    user='postgres',
    password='postgres'
)

print('Connected')

cnxn.close()

#TODO: this module/script (what makes more sense?) will be responsible for loading S3 data into postgres