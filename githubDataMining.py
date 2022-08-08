#Dependencies
#homebrew install pip3 (or any other package manager that you can get pip through)
#pip3 install PyGithub requests
#pip3 install requests beautifulsoup4
#pip3 install lxml
#pip3 install regex

import requests
from bs4 import BeautifulSoup
import lxml
import re
import time

#returns total number of file changes made in a commit.
#takes commit page as its argument
def getChurnRate(page):
    num_changes = 0
    change_num_add = 0
    change_num_delete = 0
    additions = git_page.find("strong", string=re.compile("addition")) #list type
    deletions = git_page.find("strong", string=re.compile("deletion")) #list type

    #incase we have only additions or deletions
    #so program doesn't stop because of this reason
    try:
        change_num_add = int(re.sub("[^0-9]", "", additions.string))
    except:
        change_num_delete = int(re.sub("[^0-9]", "", deletions.string))

    try:
        change_num_delete = int(re.sub("[^0-9]", "", deletions.string))
    except:
        pass

    num_changes = change_num_add + change_num_delete
    return num_changes

#takes a html_repo page (or subdirectory page)
#Returns all the files listed in that particular github page
def getFilesInPage(page):
    filepages = []
    #get all the listed files in a git repo page
    files = page.find_all("a", "js-navigation-open Link--primary")
    #print(files)
    for file in files:
        filepages.append(file.string)
    return filepages

#Takes a list of files and converts it to a dictionary
#to initialize a commit dict for recording change rate of each file
#Returns the dictionary
def initCommitDict(files):
	commit_dict = {}
	for file in files:
		commit_dict[file] = 0
	return commit_dict

#gets commit links from a particular github page
#and returns a list of links of commits for each page.
def getCommitLinks(page):
    commit_list = []
    commits = page.find_all("a", "Link--primary text-bold js-navigation-open markdown-title")
    for commit in commits:
        commit_list.append("https://github.com" + commit['href'])
    return commit_list


#takes a github commit page and returns the list of files that have been changed
#in that commit with respect to a particular directory
#if only a single file was changed, it will return the first level into the directory file name in a list
#I Know; this function isn't logical and easy to follow :(
def getCommitFilesList(page, directory='nova'):
    commit_files = []
    #if we have a bunch of files where changes occured
    file_set = page.find_all("span", "ActionList-item-label ActionList-item-label--truncate")

    #if only one file was changed
    single_file = page.find("a", "Link--primary Truncate-text")
    if file_set != []:
        for file in file_set:
            stripped_file_path = file.string.strip().split('/')
            commit_files.append(stripped_file_path[0])
    else:
        #commit_files.append(single_file)
        file_path = single_file.string.strip().split('/')
        for file_level in file_path:
            if file_level == directory:
                commit_files.append(file_level)
    return commit_files

#takes a page and extracts the date of a commit
def getCommitDate(page):
    datetime = page.find('relative-time', 'no-wrap')
    return datetime['datetime'].split('T')[0]

#takes a git commit page and extracts the month of a certaain commit
def getCommitMonth(page):
    datetime = page.find('relative-time', 'no-wrap')
    return datetime['datetime'].split('-')[1]

#takes a page of commits and gets the link to the next set of commits.
def getNextCommitsPage(page):
    next_page = page.find_all("a", "btn btn-outline BtnGroup-item")
    return next_page[-1]['href']

#to get html page of nova subdirectory and grab all the files in there
nova_page = requests.get("https://github.com/openstack/nova/tree/master/nova").text
nova = BeautifulSoup(nova_page, "lxml")
totalChurn = 0
monthlyChurn = 0
current_commit_month = 8 #since current month is August, better ways to do this though by actually getting the current date with a function

#get all the files/folders in nova subdirectory
#and starts a dictionary to keep track of any commit changes for each file
nova_files = initCommitDict(getFilesInPage(nova)) #a dictionary
commits_url = "https://github.com/openstack/nova/commits/master"
start_date = "2022-01-01" #Date to use for start of mining commits
start_date1 = time.strptime(start_date, "%Y-%m-%d")

print("Mining first page of commits... Please Wait")

endLoop = False

while endLoop == False:
    #get commits links of each page.
    commit_pages = requests.get(commits_url).text
    commits = BeautifulSoup(commit_pages, "lxml")
    commitens = getCommitLinks(commits)

    for commit in commitens:
        #print("Commit Link: ", commit)
        page = requests.get(commit).text
        git_page = BeautifulSoup(page, "lxml")
        commit_files = getCommitFilesList(git_page)

        for file in commit_files:
            if file in nova_files.keys():
                nova_files[file] += 1
        currentChurn = getChurnRate(git_page)
        totalChurn += currentChurn

        #print("Churn Rate of this commit is ", currentChurn)

        #get date of commit
        commit_date = getCommitDate(git_page)
        commit_date1 = time.strptime(commit_date, "%Y-%m-%d")

        #get the month of the commit
        commit_month = getCommitMonth(git_page)
        if int(commit_month) == current_commit_month:
            monthlyChurn += currentChurn
        #since we're starting from current month to previous months
        elif int(commit_month) < current_commit_month:
            print("Monthly Churn for ", current_commit_month, " is ", monthlyChurn)
            print("Test, Virt, Compute, : ", nova_files['tests'], nova_files['virt'], nova_files['compute'])
            current_commit_month -=1
            monthlyChurn = currentChurn

        #check if date of commit being analyzed is within the time range that we want to analyze
        if commit_date1 < start_date1:
            #print churn rate for current month being evaluated before ending program
            print("Monthly Churn for ", current_commit_month, " is ", monthlyChurn)
            endLoop = True
            break
    commits_url = getNextCommitsPage(commits)

    print("Mining next set of commits... Please wait")

print("Phewwww, Finally done!, Thanks for being patient :)")
print("The 12 most modified files of the nova subdirectory are below")

#Sorts dictionary in descending order
#Retrieved from https://careerkarma.com/blog/python-sort-a-dictionary-by-value/
sort_orders = sorted(nova_files.items(), key=lambda x: x[1], reverse=True)
length = 0
for i in sort_orders:
    print(i[0], i[1])
    #only print the 12 most modified files
    if length == 11:
        break
    length +=1

print()
print("Total Churn Rate for Studied Period is ", totalChurn)
print()
