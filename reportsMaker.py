import json
from datetime import datetime
from matplotlib import pyplot as plt
import geopandas as gpd


class ReportsMaker:
	hash_table = {}
	file_path_hash_table = "database/hash_table.json"
	current_year = datetime.now().year

	@staticmethod
	def __load_hash_table():
		with open(ReportsMaker.file_path_hash_table, 'r', encoding='utf-8') as file:
			ReportsMaker.hash_table = json.load(file)

	@staticmethod
	def create_total_bar_report():
		ReportsMaker.__load_hash_table()

		sorted_hash_table = {key: ReportsMaker.hash_table[key] for key in sorted(ReportsMaker.hash_table)}
		data = []
		for key in sorted_hash_table.keys():
			if type(sorted_hash_table[key]) is list:
				data.append({"category": key, "value": len(sorted_hash_table[key])})

		categories = [item['category'] for item in data]
		values = [item['value'] for item in data]

		plt.figure(figsize=(8, 6))  # Set the figure size
		plt.bar(categories, values, width=0.6)  # Create bars with specified width

		plt.title('Category vs Value Report')
		plt.xlabel('Category')
		plt.ylabel('Value')

		fig = plt.gcf()
		return fig

	@staticmethod
	def age_group_pie_chart():
		fig = plt.figure(figsize=(8, 6))  # Create figure
		cnps = []
		for key in ReportsMaker.hash_table.keys():
			if type(ReportsMaker.hash_table[key]) is not list:
				continue
			for item in ReportsMaker.hash_table[key]:
				cnps.append(item["cnp"])

		age_groups = {'<18': 0, '18-65': 0, '>65': 0}

		# Classify each CNP into the correct age group
		for cnp in cnps:
			group = ReportsMaker.__classify_age_group(cnp, ReportsMaker.current_year)
			if group:
				age_groups[group] += 1

		# Filter out age groups with a count of 0
		age_groups = {k: v for k, v in age_groups.items() if v > 0}

		if not age_groups:
			# Handle case where no valid data is available to plot
			plt.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
			plt.axis('off')
		else:
			# Prepare data for the pie chart
			labels = age_groups.keys()
			sizes = age_groups.values()
			plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
			plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

		return fig  # Return figure to embed in tkinter

	@staticmethod
	def __extract_birth_year(cnp):
		century_code = int(cnp[0])
		year = int(cnp[1:3])

		if century_code in [1, 2]:  # 1900–1999
			birth_year = 1900 + year
		elif century_code in [3, 4]:  # 1800–1899
			birth_year = 1800 + year
		elif century_code in [5, 6]:  # 2000–2099
			birth_year = 2000 + year
		else:
			birth_year = None  # Invalid CNP format

		return birth_year

	@staticmethod
	def __classify_age_group(cnp, current_year):
		birth_year = ReportsMaker.__extract_birth_year(cnp)

		if birth_year:
			age = current_year - birth_year

			if age < 18:
				return '<18'
			elif 18 <= age <= 65:
				return '18-65'
			else:
				return '>65'
		return None
	@staticmethod
	def __generate_county_counts(cnps):
		# Initialize dictionary to hold counts for each county
		county_counts = {f"{i:02d}": 0 for i in range(1, 53)}  # County codes from 01 to 52

		# Count occurrences for each county based on CNP
		for cnp in cnps:
			county_code = cnp[7:9]  # Extract the 8th and 9th digits
			if county_code in county_counts:
				county_counts[county_code] += 1

		# Remove entries for counties with no counts
		county_counts = {k: v for k, v in county_counts.items() if v > 0}

		return county_counts


	@staticmethod
	def classify_by_county():
		# Load the GeoJSON file
		romania_map = gpd.read_file("database/ro.json")

		ReportsMaker.__load_hash_table()

		sorted_hash_table = {key: ReportsMaker.hash_table[key] for key in sorted(ReportsMaker.hash_table)}
		data = []
		for key in sorted_hash_table.keys():
			if type(sorted_hash_table[key]) is list:
				for cnp_list in sorted_hash_table[key]:
					data.append(cnp_list["cnp"])

		county_counts = ReportsMaker.__generate_county_counts(data)

		# Mapping of GeoJSON 'id' values to county codes
		county_id_mapping = {
			"ROAB": "01",  # Alba
			"ROAR": "02",  # Arad
			"ROAG": "03",  # Argeș
			"ROBC": "04",  # Bacău
			"ROBH": "05",  # Bihor
			"ROBN": "06",  # Bistrița-Năsăud
			"ROBT": "07",  # Botoșani
			"ROBV": "08",  # Brașov
			"ROBR": "09",  # Brăila
			"ROBZ": "10",  # Buzău
			"ROCS": "11",  # Caraș-Severin
			"ROCJ": "12",  # Cluj
			"ROCT": "13",  # Constanța
			"ROCV": "14",  # Covasna
			"RODB": "15",  # Dâmbovița
			"RODJ": "16",  # Dolj
			"ROGL": "17",  # Galați
			"ROGJ": "18",  # Gorj
			"ROHR": "19",  # Harghita
			"ROHD": "20",  # Hunedoara
			"ROIL": "21",  # Ialomița
			"ROIS": "22",  # Iași
			"ROIF": "23",  # Ilfov
			"ROMM": "24",  # Maramureș
			"ROMH": "25",  # Mehedinți
			"ROMS": "26",  # Mureș
			"RONT": "27",  # Neamț
			"ROOT": "28",  # Olt
			"ROPH": "29",  # Prahova
			"ROSM": "30",  # Satu Mare
			"ROSJ": "31",  # Sălaj
			"ROSB": "32",  # Sibiu
			"ROSV": "33",  # Suceava
			"ROTR": "34",  # Teleorman
			"ROTM": "35",  # Timiș
			"ROTL": "36",  # Tulcea
			"ROVS": "37",  # Vaslui
			"ROVL": "38",  # Vâlcea
			"ROVN": "39",  # Vrancea
			"ROBU": "40",  # București
			"ROB": "41",  # București - Sector 1
			"ROB": "42",  # București - Sector 2
			"ROB": "43",  # București - Sector 3
			"ROB": "44",  # București - Sector 4
			"ROB": "45",  # București - Sector 5
			"ROB": "46",  # București - Sector 6
			"ROCL": "51",  # Călărași
			"ROGR": "52",  # Giurgiu
		}

		# Apply the mapping to create a county_code column
		romania_map['county_code'] = romania_map['id'].map(county_id_mapping)

		# Map the counts to the GeoDataFrame, setting count to 0 if county_code is None
		romania_map['count'] = romania_map['county_code'].map(lambda code: county_counts.get(code, 0))


		# Plot the map with the counts
		fig, ax = plt.subplots(1, 1, figsize=(10, 10))
		romania_map.boundary.plot(ax=ax, linewidth=1)  # Outline each county
		romania_map.plot(column='count', ax=ax, legend=False, cmap='OrRd')
		plt.title("CNP Count by County in Romania")
		plt.axis('off')
		fig = plt.gcf()
		return fig

	@staticmethod
	def gender_pie_chart():
		sorted_hash_table = {key: ReportsMaker.hash_table[key] for key in sorted(ReportsMaker.hash_table)}
		data = []
		for key in sorted_hash_table.keys():
			if type(sorted_hash_table[key]) is list:
				for cnp_list in sorted_hash_table[key]:
					data.append(cnp_list["cnp"])

		cnps = data

		# Initialize counters
		male_count = 0
		female_count = 0

		# Count genders based on the first digit (S component)
		for cnp in cnps:
			s_component = cnp[0]
			if s_component in '1357':  # Male indicators
				male_count += 1
			elif s_component in '2468':  # Female indicators
				female_count += 1

		# Data for pie chart
		labels = ['Male', 'Female']
		sizes = [male_count, female_count]
		colors = ['skyblue', 'lightcoral']

		# Plot pie chart
		plt.figure(figsize=(6, 6))
		plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
		plt.title("Gender Distribution in CNPs")
		fig = plt.gcf()
		return fig
