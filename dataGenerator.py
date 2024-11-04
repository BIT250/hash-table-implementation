import random as random

from faker import Faker


class DataGenerator:
	@staticmethod
	def generate_cnps(number_of_cnps):
		generated_cnps = []
		print("Generating cnps")
		while len(generated_cnps) != number_of_cnps:
			print(f"{len(generated_cnps)} / {number_of_cnps}")
			cnp = DataGenerator.__generate_cnp()
			if cnp not in generated_cnps:
				generated_cnps.append(cnp)

		print(f"{len(generated_cnps)} / {number_of_cnps}")

		return generated_cnps

	@staticmethod
	def __generate_cnp():
		cnp = ""

		sex = DataGenerator.__generate_sex()
		year = DataGenerator.__generate_year(sex)
		month = DataGenerator.__generate_month()
		day = DataGenerator.__generate_day(year, month)
		county = DataGenerator.__generate_county()
		secvential_number = DataGenerator.__generate_secvential_number()
		c = DataGenerator.__generate_control_digit()

		cnp += sex + year + month + day + county + secvential_number + c
		return cnp

	@staticmethod
	def __generate_sex() -> str:
		choices = ['1', '2', '5', '6', '7', '8']
		weights = [40, 40, 10, 10, 1, 1]
		return random.choice(random.choices(choices, weights, k=1000))

	@staticmethod
	def __generate_year(sex) -> str:
		if sex in ["1", "2"]:
			return str(random.randint(50, 99))
		if sex in ["5", "6"]:
			year = random.randint(0, 24)
			return str(year) if year > 9 else "0" + str(year)
		if sex in ["7", "8"]:
			year1 = random.randint(50, 99)
			year2 = random.randint(0, 24)
			year = random.choice([year1, year2])
			return str(year) if year > 9 else "0" + str(year)
		return "00"

	@staticmethod
	def __generate_month() -> str:
		month = random.randint(1, 12)
		return str(month) if month > 9 else "0" + str(month)

	@staticmethod
	def __generate_day(year, month) -> str:
		year = int(year)
		month = int(month)

		if month in [1, 3, 5, 7, 8, 10, 12]:
			day = random.randint(1, 31)
			return str(day) if day > 9 else "0" + str(day)

		if month == 2 and year % 4 == 0 and year != 0:
			day = random.randint(1, 29)
			return str(day) if day > 9 else "0" + str(day)

		if month == 2:
			day = random.randint(1, 29)
			return str(day) if day > 9 else "0" + str(day)

		if month in [4, 6, 9, 11]:
			day = random.randint(1, 29)
			return str(day) if day > 9 else "0" + str(day)

		return "00"

	import random

	@staticmethod
	def __generate_county() -> str:
		# Define counties and their codes
		counties = [x for x in range(1, 47)]
		counties.extend([51, 52])  # For Bucharest sectors

		# Population-based weights for each county (simplified for demonstration)
		# Actual values should be proportional to each county's population.
		weights = [
			0.634751, 0.462343, 0.413686, 0.735077, 0.392069, 0.250849, 0.217851, 0.136087, 0.108759, 0.267147,  # 01-10
			0.222449, 0.735077, 0.263688, 0.146921, 0.209027, 0.123245, 0.217851, 0.137389, 0.200042, 0.217899,  # 11-20
			0.375507, 0.231234, 0.304332, 0.176958, 0.185122, 0.197303, 0.189457, 0.245436, 0.274352, 0.278916,  # 21-30
			0.221514, 0.298323, 0.171167, 0.213251, 0.122789, 0.179587, 0.150491, 0.232753, 0.238709, 1.716961,  # 31-40 (40: București)
			0.899999, 0.899999, 0.899999, 0.899999, 0.286261, 0.286261, 0.125912, 0.125912  # 41-46 + 51, 52
		]

		county = random.choices(counties, weights=weights, k=1)[0]
		return str(county) if county > 9 else "0" + str(county)

	@staticmethod
	def __generate_secvential_number() -> str:
		numbers = list(range(1, 1000))
		weights = [5 if 1 <= num <= 200 else 1 for num in numbers]
		secvential_number = random.choices(numbers, weights, k=1000)[0]

		if secvential_number < 10:
			return "00" + str(secvential_number)
		elif secvential_number < 100:
			return "0" + str(secvential_number)
		else:
			return str(secvential_number)

	@staticmethod
	def __generate_control_digit() -> str:
		return str(random.randint(0, 9))

	@staticmethod
	def __generate_name(cnp) -> str:
		fake = Faker('ro_RO')
		sex = cnp[0]
		if sex in "1357":
			return fake.name_male()
		else:
			return fake.name_female()

	@staticmethod
	def generate_persons(no_of_persons):
		persons = []
		cnp_list = DataGenerator.generate_cnps(no_of_persons)
		print("Generate names")
		for cnp in cnp_list:
			name = DataGenerator.__generate_name(cnp)
			persons.append(cnp + "," + name)
			print(f"{len(persons)}/{no_of_persons}")

		return persons

	