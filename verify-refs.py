import argparse
import sys
import configparser
from pprint import pprint

def help(show=False):
	parser = argparse.ArgumentParser(description="")
	configs = parser.add_argument_group('System settings', 'System parameters to run the system in the different modes')
	configs.add_argument('-s', '--settings', dest='settings', \
						type=str, default="settings.ini", \
						help='The system settings file (default: settings.ini)')	
	if show:
		parser.print_help()
	return parser.parse_args()

def readSettings(settingsFile):
	configuration = configparser.ConfigParser()
	configuration.read(settingsFile)
	if not configuration:
		raise Exception("The settings file was not found!")
	return configuration._sections

def checkDuplicatedRefs(bibFile):
	stats = {
		"articles":0,
		"inproceedings":0,
		"others":0,
		"duplicated":[],
		"missing_doi":[],
		"titles_without_quotes":[]
	}
	titles = []
	containsDoi=False
	currentTitle=""
	file = open(bibFile, 'r')
	for rline in file.readlines():
		NEW=True
		line = rline.lstrip()
		if "@article" in line:
			stats["articles"] += 1
		elif "@inproceedings" in line:
			stats["inproceedings"] += 1
		elif line.startswith("@"):
			stats["others"] += 1
		else:
			NEW=False

		if NEW:
			containsDoi=False

		if line.startswith("title="):
			currentTitle = line
			title = line.replace(" ", "")
			title = title.replace("\"", "")
			if title in titles:
				stats["duplicated"].append(line)
			titles.append(title)
			if "title=\"{" not in line:
				stats["titles_without_quotes"].append(line)

		if "doi=" in line:
			containsDoi=True
		
		if line.startswith("}") and not containsDoi:
			stats["missing_doi"].append(currentTitle)

	pprint(stats, width=200)


def main():
	args = help()
	settings = readSettings(args.settings)
	bibFile = settings["bib"]["file"]
	checkDuplicatedRefs(bibFile)

if __name__ == '__main__':
	if "/" in sys.argv[0]:
		print("ERROR: Please run this script in the right path!")
	else:
		main()
