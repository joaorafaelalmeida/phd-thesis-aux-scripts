import argparse
import sys
import configparser

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

def main():
	args = help()
	settings = readSettings(args.settings)
	print(settings)

if __name__ == '__main__':
	if "/" in sys.argv[0]:
		print("ERROR: Please run this script in the right path!")
	else:
		main()
