from fabric.api import local, settings, abort
from fabric.contrib.console import confirm


# prep

def test():
	# result = local("nosetests -v")
	with settings(warn_only=True):
		# result = local("python test_tasks.py -v && python test_users.py -v", 
		#	capture=True)
		result = local("nosetests -v", capture=True)
	if result.failed and not confirm("Tests failed. Continue?"):
		abort("Aborted at user request.")

def commit():
	message = raw_input("Enter a git commit message: ")
	# local("git add . && git commit -am '{}'".format(message))
	# local('git add . && git commit -am "Building a REST API"')
	local('git add . && git commit -am "' + message + '"')

def push():
	local("git branch")
	message = str(raw_input("Enter a branch to push: "))
	# local('git push origin master')
	# local("git push -u origin '{}'".format(message))
	local("git push -u origin {}".format(branch))

def prepare():
	test()
	commit()
	push()


# deploy

def pull():
	local("git pull origin master")

def heroku():
	local("git push heroku master")

def heroku_test():
	local("heroku run python test_tasks.py -v && heroku run python test_users.py -v")

def deploy():
	pull()
	test()
	commit()
	heroku()
	heroku_test()


# rollback

def rollback():
	local("heroku rollback")