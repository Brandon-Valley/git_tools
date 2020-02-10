import ntpath
import time


import Git_Commit



# to import from parent dir
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..\\..')) 

# from parent dir
from submodules.exception_utils import exception_utils as eu
from submodules.subprocess_utils import subprocess_utils as su
	
	

	
	
def cd(dir_path):
	os.chdir(dir_path)
	
	
class Git_Repo:
	def __init__(self, repo_path, remote_base_url = None):
		self.path     = repo_path
		self.name     = ntpath.basename(self.path)
		self.commit_l = []
		self.url      = None
		
		if remote_base_url != None:
			self.url = remote_base_url + '//' + self.name
		
		
	
	def run_git_cmd(self, cmd, print_output = False, print_cmd = False, sleep = 0, shell = False, run_type = 'popen', decode = False):
# 		if run_type not in ['popen']
		eu.error_if_param_invalid(run_type, ['popen', 'call'])
		
		og_cwd = os.getcwd()
		cd(self.path)
		
		if run_type == 'popen':
			output = su.run_cmd_popen(cmd, print_output, print_cmd, shell, decode)
		elif run_type == 'call':
			output = su.run_cmd_call (cmd, print_cmd, shell, decode)
		
		if sleep > 0:
			if print_output:
				print('  Sleeping For ', sleep, ' Seconds...')
			time.sleep(sleep)
		
		cd(og_cwd) # return to original cwd
		return output
			



	''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
	'''                                                                           
	        Basic Commands - One Arg
	'''
	''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''

	def commit_simple        (self, msg        , print_output = False, print_cmd = False):  self.run_git_cmd('git commit -a -m "' + msg + '"'   , print_output
																											   									, print_cmd)
	def checkout_simple      (self, branch_name, print_output = False, print_cmd = False):  self.run_git_cmd('git checkout ' + branch_name      , print_output
																																				, print_cmd)
	# adds repo at the given URL as a submodule of this repo
	def add_submodule_simple (self, repo_url   , print_output = False, print_cmd = False):  self.run_git_cmd('git submodule add' + repo_url     , print_output
																																				, print_cmd)
	# merges given branch name into current branch without fast-forwarding
	def merge_no_ff          (self, branch_name, print_output = False, print_cmd = False):  self.run_git_cmd('git merge --no-ff ' + branch_name , print_output
																																				, print_cmd
																																				, sleep = 0.5) # not optimized

	''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
	'''                                                                           
	        Basic Commands - No Args
	'''
	''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''

	def flow_init_default (self, print_output = False, print_cmd = False):  self.run_git_cmd('git flow init -d -f' , print_output
																												   , print_cmd)
	def add_all_files     (self, print_output = False, print_cmd = False):  self.run_git_cmd('git add .'           , print_output
																												   , print_cmd)
	def push_all_branches (self, print_output = False, print_cmd = False):  self.run_git_cmd('git push --all'      , print_output
																												   , print_cmd)

	''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
	'''                                                                           
	        Specific Utility Commands - Return
	'''
	''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''

	# most recent commit at position 0
	def get_abrv_commit_hash_l (self, print_output = False, print_cmd = False):  
		raw_l = self.run_git_cmd('git log --oneline --pretty=format:"%h"', print_output , print_cmd, decode = True)
		
		abrv_commit_hash_l = []
		for line in raw_l:
			abrv_commit_hash_l.append(line.rstrip())
		return abrv_commit_hash_l


	# returns T / F if a git repo has already been initialized in self.path
	# returns False if path does not exist
	def exists(self):
		if not os.path.isdir(self.path):
			return False

		og_cwd = os.getcwd()
		cd(self.path)
		
		repo_exists = not su.fatal_error('git rev-parse --is-inside-work-tree')
		cd(og_cwd) # return to original cwd
		return repo_exists


	''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
	'''                                                                           
	        Internal Build Commands
	'''
	''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''

	def build_commit_l(self): 
		abrv_commit_hash_l = self.get_abrv_commit_hash_l()
		for abiv_commit_hash in abrv_commit_hash_l:
			c = Git_Commit.Git_Commit(abiv_commit_hash, self.run_git_cmd)
			self.commit_l.append(c)

		print('# of commits in commit_l:  ', len(self.commit_l))#````````````````````````````````````````````````````````````````````````````````````````````````

# 	def init_commit(self, abrv_commit_hash):




# 
# 
# def run_git_cmd(repo_path, cmd, print_output = False, print_cmd = False):
# 	cd(repo_path)
# 	run_cmd(cmd, print_output, print_cmd)
# 	
# 	
# 	
# 	
# 	
# def commit(repo_path, msg, options_str = ''):
# 	# options_str = ''
# 	# for option in option_l:
# 		# options_str += ' ' + option + ' '
# 		
# 	cd(repo_path)
# 	cmd = 'git commit ' + options_str + ' -m "' + msg + '"'
# 	# cmd_out = subprocess.check_output(cmd, shell = False)
# 	# print(cmd_out)
# 	
# 	run_cmd(cmd, print_output = True)
# 	
# 	
# def add(repo_path, options_str = ''):
# 	cd(repo_path)
# 	cmd = 'git add ' + options_str
# 	# cmd_out = subprocess.check_output(cmd, shell = False)
# 	# print(cmd_out)
# 	
# 	run_cmd(cmd, print_output = True)
# 	
# 	
# 
# 	
# '''
# # adds and commits all files in existing repo at repo_path with given msg
# def commit_all_files(repo_path, msg):
# 	cd(repo_path)
# 	cmd = 'git add .'
# 	print(subprocess.check_output(cmd, shell = False))
# 	
# 	cmd = 'git commit -m "' + msg + '"'
# 	print(subprocess.check_output(cmd, shell = False))
# '''
# 	
# # adds the existing repo at submodule_repo_url as a submodule of the existing repo at top_lvl_repo_path
# # submodule repo must have at least one commit (does not need to have been pushed)
# def add_submodule(top_lvl_repo_path, submodule_repo_url):
# 	cd(top_lvl_repo_path)
# 	# print('\n  in git_utils, in ' , top_lvl_repo_path, '  ,about to add submodule... \n')#`````````````````````````````````````````````````
# 	cmd = 'git submodule add ' + submodule_repo_url
# 	# print(cmd)
# 	# print(subprocess.check_output(cmd))
# 	run_cmd(cmd, print_output = True)
# 	
# 	
# def add_branch(repo_path, branch_name):
# 	cd(repo_path)
# 	cmd = 'git branch ' + branch_name
# 	run_cmd(cmd, print_output = True, print_cmd = True)
# 	
# 	
# def checkout_branch(repo_path, branch_name):
# 	cd(repo_path)
# 	cmd = 'git checkout ' + branch_name
# 	run_cmd(cmd, print_output = True, print_cmd = True)
# 	
# # merges the branch you are in into branch_name_to_merge_into
# def merge_branch(repo_path, branch_name_to_merge_into, options_str = ''):
# 	cd(repo_path)
# 	cmd = 'git merge ' + options_str + ' ' + branch_name_to_merge_into
# 	run_cmd(cmd, print_output = True, print_cmd = True)
# 	
# 	
# def tag(repo_path, tag_name):
# 	cd(repo_path)
# 	cmd = 'git tag ' + tag_name
# 	run_cmd(cmd, print_output = True, print_cmd = True)
# 	
# 	
# def add_all(repo_path):  
# 	add(repo_path, ' . ')
# 	
# 
# 	
# 	
# # adds existing, brand new, empty repo as a submodule of existing repo
# def add_new_repo_as_submodule(top_lvl_repo_path, submodule_repo_path, submodule_repo_url):
# 	add_all(submodule_repo_path) # need
# 	commit(submodule_repo_path, 'Initialized Repository', ' --allow-empty ')
# 	
# 	add_submodule(top_lvl_repo_path, submodule_repo_url)
# 	
# 	add_all(top_lvl_repo_path)
# 	commit_msg = "Initialized repository as submodule:  " + ntpath.basename(submodule_repo_path)
# 	commit(top_lvl_repo_path, commit_msg)
# 	
	
	
	
def main():
# 	SUBMODULE_REPO_PATH = "C:\\Users\\mt204e\\Documents\\test\\git_test\\repo_from_command_line_test_dir\\ip_test_from_cmd_0\\submodule_repo"
# 	SUBMODULE_REPO_URL = "https://ba-bit.web.boeing.com/users/mt204e/repos/submodule_repo"
# 	TOP_LVL_REPO_PATH = "C:\\Users\\mt204e\\Documents\\test\\git_test\\repo_from_command_line_test_dir\\ip_test_from_cmd_0"
# 	
# 	# commit_all_files(SUBMODULE_REPO_PATH, 'Initialized Repository')
# 	# add_submodule(TOP_LVL_REPO_PATH, SUBMODULE_REPO_URL)
# 	
# 	add_new_repo_as_submodule(TOP_LVL_REPO_PATH, SUBMODULE_REPO_PATH, SUBMODULE_REPO_URL)
# 	

	g = Git_Repo("C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\\ip_repo")
# 	g.run_git_cmd('git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n H   commit hash: ', print_output = True, print_cmd = True)
	g.build_commit_l()

# 	g.run_git_cmd('git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n H   commit hash: ', print_output = True, print_cmd = True, run_type = "call")
	
# 	g.run_git_cmd('git log 34f2fab -n1 --oneline > C:\Users\mt204e\Documents\projects\Bitbucket_repo_setup\svn_to_git_ip_repo\test_log.txt')
# 	import subprocess
# 	cd(g.path)
# 	
# # 	p = subprocess.Popen(['git', 'log',  '34f2fab',  '-n1',  '--oneline ', ' > ',  "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\\test_log.txt"])
# 	
# # 	subprocess.call('git log 34f2fab -n1 --oneline --pretty=format:"COMMIT_HASH:%h  BODY: %b  COMMIT_NOTES: %n SUBJECT: %s  AUTHOR_DATE: %ad" > "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\\test_log.txt"' , shell = True)
# 	su.run_cmd('git log 34f2fab -n1 --oneline --pretty=format:"COMMIT_HASH:%h  BODY: %b  COMMIT_NOTES: %n SUBJECT: %s  AUTHOR_DATE: %ad" > "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\\test_log.txt"', shell=True )
# 
# # 	print('git log 34f2fab -n1 --oneline --pretty=format:"COMMIT_HASH: %h\n  BODY: %b\n  COMMIT_NOTES: %n SUBJECT: %s  AUTHOR_DATE: %ad" > C:\Users\mt204e\Documents\projects\Bitbucket_repo_setup\svn_to_git_ip_repo\test_log.txt')
# # 	import os
# # 	os.system('git log 34f2fab -n1 --oneline --pretty=format:"COMMIT_HASH:\n\n\n %h  BODY: %b  COMMIT_NOTES: %n SUBJECT: %s  AUTHOR_DATE: %ad" > "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\\test_log.txt"' )
# 	
	
	
if __name__ == '__main__':
# 	import repo_transfer
# 	repo_transfer.main()
	

# 	r = Git_Repo("C:\\Users\\mt204e\\Documents\\test\\git_test\\tr0")
# 	print(r.exists())
# 	
# 	r = Git_Repo("C:\\Users\\mt204e\\Documents\\test")
# 	print(r.exists())

	main()
	
	# git commit --allow-empty -m "manual first commit from cmd line"
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	