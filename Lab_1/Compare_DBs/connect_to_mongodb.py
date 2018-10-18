from pymongo import MongoClient
import time 

def create_a_number_of_collections(client):
	db = client["test_database"]
	col_name = 'col'
	for i in range(0, 400):
		col = db['{}'.format(col_name+str(i))]
		my_dict = {'number': 100}
		col.insert_one(my_dict)

		
def insert_in_the_collections(client):
	db = client["test_database"]
	col_name = 'col'
	for i in range(0, 400):
		col =  db['{}'.format(col_name+str(i))]
		my_dict = {'number': 300}
		col.insert_one(my_dict)

def drop_collection(client):
	db = client["test_database"]
	col_name = 'col'
	for i in range(0, 400):
		db.drop_collection('{}'.format(col_name+str(i)))

def main():
	client = MongoClient()
	dblist = client.list_database_names()
	if "test_database" in dblist:
		print("The database exists.")
	else:
		db = client["test_database"]

	s = time.time()
	create_a_number_of_collections(client)
	e = time.time()
	print('COMPARE Create: ', e-s)

	s = time.time()
	insert_in_the_collections(client)
	e = time.time()
	print('COMPARE Insert: ', e-s)

	s = time.time()
	drop_collection(client)
	e = time.time()
	print('COMPARE Drop Collection: ', e-s)



if __name__ == '__main__':
	main()