# How to Use

Be sure to have python 3.6 installed on your computer

Create the list-repo.py file in a folder on your computer and copy the content of the #list-repos.py file to it and save

Open your terminal and run python ./list-repo.py -u <username> --token "<insert token>" where you replace with the username you wish to list the repositories from and token is your GithubApi token

If you do not specify a username, it will default to the github user and list its public repositories

E.g.

python ./list-repo.py -u dareogunewu --token "06495ab473864c75a6f4b6d6c148d9b039ab5a03"
