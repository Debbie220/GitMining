# GitMining
<p>This project is a tool meant for retrieving data on the commits made to the <a href="https://github.com/openstack/nova" target="_blank">openstack Nova project</a>.</p>
<p>More specifically, it is designed to retrieve data about the frequency of commits made to files within the <a href="https://github.com/openstack/nova/nova" target="_blank">nova subdirectory</a> of the Nova project.</p>
<p>It analyzes the commits of the project over the last 6 months and it gives a summary of the twelve most edited files of the nova subdirectory and also the churn rate
(total number of additions and deletions of whole project) for the specified time period.
This program can also be easily edited to analyze the rate of commits for longer periods e.g. the past year.</p>
<p>Please check out the file dependencies.txt for a list of what packages are needed for this program to work</p>
<p>From the command line, just need to run "python3 githubDataMining.py" for the program to be executed</p>
