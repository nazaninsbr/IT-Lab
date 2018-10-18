import sqlite3
import time

def create_a_number_of_tables(db, c):
	table_name = 't'
	col_name = 'col1'
	field_type = 'INTEGER'
	for i in range(0, 400):
		c.execute('CREATE TABLE {tn} ({nf} {ft})'\
		.format(tn=table_name+str(i), nf=col_name, ft=field_type))

def insert_in_the_tables(db, c):
	table_name = 't'
	for i in range(0, 400):
		c.execute('INSERT INTO {tn}(col1) VALUES(100)'.format(tn=table_name+str(i)))

def update_the_tables(db, c):
	table_name = 't'
	for i in range(0, 400):
		c.execute('UPDATE {tn} SET (col1)=(200) WHERE col1=(100)'.format(tn=table_name+str(i)))

def drop_table(db, c):
	table_name = 't'
	for i in range(0, 400):
		c.execute('DROP TABLE {tn}'.format(tn=table_name+str(i)))

def main():
	my_sqlite = './my_db.sqlite'
	conn = sqlite3.connect(my_sqlite)
	c = conn.cursor()

	s = time.time()
	create_a_number_of_tables(conn, c)
	e = time.time()
	print('COMPARE Create: ', e-s)
	conn.commit()

	s = time.time()
	insert_in_the_tables(conn, c)
	e = time.time()
	print('COMPARE Insert: ', e-s)
	conn.commit()

	s = time.time()
	update_the_tables(conn, c)
	e = time.time()
	print('COMPARE Update: ', e-s)
	conn.commit()

	s = time.time()
	drop_table(conn, c)
	e = time.time()
	print('COMPARE Drop Table: ', e-s)
	conn.commit()

	conn.close()


if __name__ == '__main__':
	main()