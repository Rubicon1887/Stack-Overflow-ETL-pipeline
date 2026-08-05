import psycopg

cnxn=psycopg.connect(
    host='localhost',
    dbname='stkof',
    user='postgres',
    password='postgres'
)

print('Connected')

cnxn.close()

# TODO: Cree a SQL file to create postgres tables