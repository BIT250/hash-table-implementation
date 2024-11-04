import json
import random


class TableManagement():
	file_path_persons = "database/persons.txt"
	file_path_hash_table = "database/hash_table.json"

	hash_table = {}
	hash_size = 0
	persons = []
	persons_to_find = []
	no_of_persons_to_find = 0

	@staticmethod
	def save_data(data):
		file = open(TableManagement.file_path_persons, "w", encoding="utf-8")
		for item in data:
			file.write(f"{item}\n")

	@staticmethod
	def __load_persons():
		file = open(TableManagement.file_path_persons, "r", encoding="utf-8")

		for line in file:
			person = line.split(",")
			TableManagement.persons.append({"cnp": person[0], "name": person[1].strip()})

	@staticmethod
	def __load_hash_table():
		with open(TableManagement.file_path_hash_table, 'r', encoding='utf-8') as file:
			TableManagement.hash_table = json.load(file)


	@staticmethod
	def generate_hash_table(hash_method):
		TableManagement.__load_persons()
		no_of_hash_codes = int(len(TableManagement.persons) ** 0.5)
		TableManagement.hash_size = no_of_hash_codes
		TableManagement.no_of_persons_to_find = int(len(TableManagement.persons) ** 0.5)
		TableManagement.persons_to_find = random.sample(TableManagement.persons, TableManagement.no_of_persons_to_find)
		for person in TableManagement.persons:
			cnp = person["cnp"]

			match hash_method:
				case 1:
					hash_code = TableManagement.__hash_function_1(cnp, no_of_hash_codes)
					TableManagement.hash_table["method"] = 1

				case 2:
					hash_code = TableManagement.__hash_function_2(cnp, no_of_hash_codes)
					TableManagement.hash_table["method"] = 2
				case _:
					hash_code = TableManagement.__hash_function_1(cnp, no_of_hash_codes)
					TableManagement.hash_table["method"] = 1

			if hash_code in TableManagement.hash_table.keys():
				TableManagement.hash_table[hash_code].append(person)
			else:
				TableManagement.hash_table[hash_code] = [person]

		with open(TableManagement.file_path_hash_table, 'w', encoding='utf-8') as file:
			json.dump(TableManagement.hash_table, file, ensure_ascii=False, indent=4)

	@staticmethod
	def __hash_function_1(cnp, n) -> int:
		return (int(cnp[0:3]) + int(cnp[3:6]) + int(cnp[6:9]) + int(cnp[9:12]) + int(cnp[12])) % n

	@staticmethod
	def __hash_function_2(cnp, n) -> int:
		hash_code = 0
		prime = 31

		for char in cnp:
			hash_code = (hash_code * prime + ord(char)) % n

		return hash_code

	@staticmethod
	def find_persons_hash_table():

		no_of_persons_to_find = int(len(TableManagement.persons) ** 0.5)
		persons_to_find = TableManagement.persons_to_find

		print(f"Finding {no_of_persons_to_find} persons in {len(TableManagement.persons)} entities using Hash Table Method {TableManagement.hash_table['method']}")

		total_iterations = 0
		for person_to_find in persons_to_find:
			match TableManagement.hash_table["method"]:
				case 1:
					hash_code = TableManagement.__hash_function_1(person_to_find["cnp"], TableManagement.hash_size)			# HASH FUNCTION
				case 2:
					hash_code = TableManagement.__hash_function_2(person_to_find["cnp"], TableManagement.hash_size)
				case _:
					hash_code = TableManagement.__hash_function_1(person_to_find["cnp"], TableManagement.hash_size)
			iterations = 0
			gasit = False
			for person in TableManagement.hash_table[hash_code]:
				iterations += 1
				if person_to_find["cnp"] == person["cnp"]:
					print(f"CNP: {person_to_find['cnp']} Name: {person_to_find['name']} found with hash_code: {hash_code} in {iterations} iterations")
					total_iterations += iterations
					gasit = True
					break
			if gasit is False:
				print(f"Person not found CNP:{person_to_find['cnp']}")

		print(f"Total iterations with hash table: {total_iterations}")
		return total_iterations

	@staticmethod
	def find_persons():
		no_of_persons_to_find = int(len(TableManagement.persons) ** 0.5)
		persons_to_find = TableManagement.persons_to_find

		print(f"\n\nFinding {no_of_persons_to_find} persons in {len(TableManagement.persons)} entities")

		total_iterations = 0
		for person_to_find in persons_to_find:
			iterations = 0
			gasit = False
			for person in TableManagement.persons:
				iterations += 1
				if person_to_find["cnp"] == person["cnp"]:
					print(f"CNP: {person_to_find['cnp']} Name: {person_to_find['name']} found in {iterations} iterations")
					total_iterations += iterations
					gasit = True
					break
			if gasit is False:
				print(f"Person not found CNP:{person_to_find['cnp']}")

		print(f"Total iterations without hash table: {total_iterations}")
		return total_iterations
