#Dependencies
#pip3 install PyGithub requests
#pip3 install requests beautifulsoup4
#pip3 install lxml
#pip3 install regex

import requests
from pprint import pprint
from bs4 import BeautifulSoup
import lxml
import re

#/repos/{owner}/{repo}/commits
# github username
owner_repo = "openstack/nova"
time = "2022-01-01T00:00:01Z"
token = "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"
headers = headers = {'Authorization':"Token "+token}

#to get html page of nova subdirectory and grab all the files in there
nova_page = requests.get("https://github.com/openstack/nova/tree/master/nova").text
nova = BeautifulSoup(nova_page, "lxml")

# url to request for commits done
url = f"https://api.github.com/repos/{owner_repo}/commits?per_page=2"
rate_limit = f"https://api.github.com/rate_limit"

# make the request and return the json
user_data = requests.get(url, headers).json()
commit_refs = []
commit_count_dict = {}

#adding the html refs to a list to be used to get more data from the pages
for commit in range(len(user_data)):
	commit_refs.append(user_data[commit]['parents'][0]['html_url'])
#rates = requests.get(rate_limit, headers).json()




#returns total number of file changes made in a commit.
def getChurnRate(page):
	num_changes = 0
	additions = git_page.find("strong", string=re.compile("additions")) #list type
	deletions = git_page.find("strong", string=re.compile("deletions")) #list type
	#print(additions.string)
	#print(deletions.string)
	change_num = re.sub("[^0-9]", "", additions.string)
	num_changes+=int(change_num)
	change_num = re.sub("[^0-9]", "", deletions.string)
	num_changes+=int(change_num)
	return num_changes

#print(getChurnRate(git_page))

#Should return all the files listed in a gitHub repo page
def getFilesInPage(page):
	filepages = []
	#get all the listed files in a git repo page
	files = page.find_all("a", "js-navigation-open Link--primary")

	for file in files:
		filepages.append(file.string.strip())
	return filepages

#returns only the first level of the folder name
#for example compute/name/folder would return only compute
#takes a string folder name as input
def getMainDirectory(folder):
	top_level_name= ''
	for letter in folder:
		if letter == '/':
			return top_level_name
		else:
			top_level_name+=letter

#takes a file path and checks if the main level is the nova directory
#returns true or false
def isNova(folder):
	folderpath = folder.split()
	print("folderPath ", folderpath)
	if folderpath[0] == 'nova':
		return true
	else
		return False

#takes a folder or file name string input and checks if it is the the
#nova subdirectory
#returns true or false
def inNovaDirectory(folder):
	stripped_file_name = getMainDirectory(folder.string.strip())
	if stripped_file_name in nova_pages:
		if stripped_file_name in commit_count_dict.keys():
			commit_count_dict[stripped_file_name] += 1
		else:
			commit_count_dict[stripped_file_name] = 1
	elif stripped_file_name == 'nova':
		print('nova')

nova_pages = getFilesInPage(nova)

#Takes a list of files and converts it to a dictionary
#to initialize a commit dict
#Returns the dictionary
def initCommitDict(files):
	commit_dict = {}
	for file in files:
		commit_dict[file] = 0
	return commit_dict

for gitpage in commit_refs:
	print(gitpage)
	git = requests.get(gitpage).text
	#print(commit_refs[1])
	# Parse the html content
	git_page = BeautifulSoup(git, "lxml")

	#to get list of files changed for each commit
	#print(git_page.find_all("span"))
	#ActionList-item-label ActionList-item-label--truncate

	#if we have a bunch of files where changes occured
	file_set = git_page.find_all("span", "ActionList-item-label ActionList-item-label--truncate")
	#print("file_set ", file_set)

	#if we have only one where changes occured
	file2 = git_page.find_all("a", "Link--primary Truncate-text")
	#print("file2 ", file2)

	#get all the files involved in the commmit
	if file_set != []:
		for file in file_set:
			print(file.string.strip())
			stripped_file_path = getMainDirectory(file.string.strip())

			if isNova(stripped_file_path) == True:
				#then I would want to now get the first level in for the folder and then
				#compare it with nova_pages.
				#stripped_file_path.split()[1]

			#if file name or directory is part of the nova subdirectory
			if stripped_file_path in nova_pages:
				if stripped_file_path in commit_count_dict.keys():
					commit_count_dict[stripped_file_path] += 1
				else:
					commit_count_dict[stripped_file_path] = 1
			else:
				continue
		print(commit_count_dict)
	else:
		#print(file)
		stripped_file_path = getMainDirectory(file2[0].string.strip())
		print(stripped_file_path)
		if stripped_file_path in nova_pages:
			if stripped_file_path in commit_count_dict.keys():
				commit_count_dict[stripped_file_path] += 1
			else:
				commit_count_dict[stripped_file_path] = 1
print(commit_count_dict)
