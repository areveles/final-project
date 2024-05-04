# final-project
# Using git commands in your terminal 
initilize your local directory where you want project folder to be located where
'yourbranchname' is your desired local branch name otherwise git init will init the branch as main
git init -b 'yourbranchname'

add the remote repository into your newly initialized branch
git remote add upstream https://www.github.com/areveles/final-project

fetch changes from remote repo
git fetch upstream

fetch changes from desired branch in repo
git fetch origin <branchname>

move to the branch you want to work from
git checkout <branchname>

to see a list of branches in the origin repo
git ls-remote

to merge files from repo to local 
git merge origin/<branch-name>

