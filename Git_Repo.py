''' -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV -- All Utilities Standard Header -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV -- '''
import sys, os    ;     sys.path.insert(1, os.path.join(sys.path[0], os.path.dirname(os.path.abspath(__file__)))) # to allow for relative imports, delete any imports under this line

util_submodule_l = ['subprocess_utils'] # list of all imports from local util_submodules that could be imported elsewhere to temporarily remove from sys.modules

# temporarily remove any modules that could conflict with this file's local util_submodule imports
og_sys_modules = sys.modules    ;    pop_l = [] # save the original sys.modules to be restored at the end of this file
for module_descrip in sys.modules.keys():  
    if any( util_submodule in module_descrip for util_submodule in util_submodule_l )    :    pop_l.append(module_descrip) # add any module that could conflict local util_submodule imports to list to be removed from sys.modules temporarily
for module_descrip in pop_l    :    sys.modules.pop(module_descrip) # remove all modules put in pop list from sys.modules
util_submodule_import_check_count = 0 # count to make sure you don't add a local util_submodule import without adding it to util_submodule_l

''' -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV -- All Utilities Standard: Local Utility Submodule Imports  -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV -- '''

from util_submodules__gu.subprocess_utils import subprocess_utils as su    ; util_submodule_import_check_count += 1 
    
''' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ '''
if util_submodule_import_check_count != len(util_submodule_l)    :    raise Exception("ERROR:  You probably added a local util_submodule import without adding it to the util_submodule_l")
''' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ '''



import ntpath
import time


try:
    # for eclipse code-completion 
    from submodules.git_tools import Git_Commit
except:
    import Git_Commit


# to import from parent dir
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..\\..')) 

# fix this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# from parent dir
from submodules.exception_utils import exception_utils as eu
from submodules.subprocess_utils import subprocess_utils as su
from submodules.logger import json_logger, txt_logger
from submodules.file_system_utils import  file_system_utils as fsu
    
    
COMMIT_L_LOG_JSON_FILE_PATH = 'commit_l.json'
LOAD_COMMIT_L_FROM_JSON_FILE_IF_EXISTS = False
LOG_COMMIT_L = False

    
    
def cd(dir_path):
    os.chdir(dir_path)
    
    
class Git_Repo:
    def __init__(self, repo_path, remote_base_url = None):
        self.path        = repo_path
        self.name        = ntpath.basename(self.path)
        self.commit_l    = []
        self.url         = None
        self.submodule_l = []
    
        if remote_base_url != None:
            self.url = remote_base_url + '//' + self.name
        
        self.init_submodule_l()
        
        
        
    def run_git_cmd(self, cmd, print_output = False, print_cmd = False, sleep = 0, shell = False, run_type = 'popen', decode = False):
    #         if run_type not in ['popen']
        eu.error_if_param_key_not_in_whitelist(run_type, ['popen', 'call'])
        
        og_cwd = os.getcwd()
        cd(self.path)
        
        if run_type == 'popen':
            output = su.run_cmd_popen(cmd, print_output, print_cmd, shell, decode)
        elif run_type == 'call':
            output = su.run_cmd_call (cmd, print_cmd, shell)
        
        if sleep > 0:
            if print_output:
                print('  Sleeping For ', sleep, ' Seconds...')
            time.sleep(sleep)
        
        cd(og_cwd) # return to original cwd
        
        
        return output
    
    

    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Basic Commands - No Args
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    
    def flow_init_default (self, print_output = False, print_cmd = False):  self.run_git_cmd('git flow init -d -f', print_output
                                                                                                                  , print_cmd)
    def add_all_files     (self, print_output = False, print_cmd = False):  self.run_git_cmd('git add .'          , print_output
                                                                                                                  , print_cmd)
    def push_all_branches (self, print_output = False, print_cmd = False):  self.run_git_cmd('git push --all'     , print_output
                                                                                                                  , print_cmd)
    def undo_checkout     (self, print_output = False, print_cmd = False):  self.run_git_cmd('git switch -'       , print_output
                                                                                                                  , print_cmd)    
    
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Basic Commands - One Arg
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    
    def commit_simple         (self, msg                , print_output = False, print_cmd = False):  self.run_git_cmd('git commit -a -m "' + msg + '"'       , print_output
                                                                                                                                                             , print_cmd)
    def checkout_simple       (self, branch_name        , print_output = False, print_cmd = False):  self.run_git_cmd('git checkout ' + branch_name          , print_output
                                                                                                                                                             , print_cmd)
    # adds repo at the given URL as a submodule of this repo
    def add_submodule_simple  (self, repo_url           , print_output = False, print_cmd = False):  self.run_git_cmd('git submodule add' + repo_url         , print_output
                                                                                                                                                             , print_cmd)
    # merges given branch name into current branch without fast-forwarding 
    def merge_no_ff           (self, branch_name        , print_output = False, print_cmd = False):  self.run_git_cmd('git merge --no-ff ' + branch_name     , print_output
                                                                                                                                                             , print_cmd
                                                                                                                                                             , sleep = 0.5) # not optimized    
    def delete_commit_history (self, push_changes = True, print_output = False, print_cmd = False):  
                                                                                                    self.run_git_cmd('git checkout --orphan latest_branch'   , print_output, print_cmd) # Checkout 
                                                                                                    self.run_git_cmd('git add -A'                            , print_output, print_cmd) # Add all the files
                                                                                                    self.run_git_cmd('git commit -am "about to del history"' , print_output, print_cmd) # Commit the changes
                                                                                                    self.run_git_cmd('git branch -D master'                  , print_output, print_cmd) # Delete the branch
                                                                                                    self.run_git_cmd('git branch -m master'                  , print_output, print_cmd) # Rename the current branch to master
                                                                                                    if push_changes:
                                                                                                        self.run_git_cmd('git push -f origin master'         , print_output, print_cmd) # Finally, force update your repository
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Basic Commands - Many Args
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''  
    def commit_full(self, msg, author, date, print_output = False, print_cmd = False):  self.run_git_cmd('git commit -a -m "' + msg    + '"'
                                                                                                         + ' --author="'      + author + '"'
                                                                                                         + ' --date="'        + date   + '"'
                                                                                                         , print_output, print_cmd)
    
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Class Commands - Takes Git_Repo and/or Git_Commit as params
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    
    def add_as_submodule(self, sm_repo):
        
    #         print('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV')#`````````````````
    #         
#         sm_repo.get_abrv_commit_hash_l()
        print('NOT IMPLEMENTED YET')
        
    #         
    #     add_all(submodule_repo_path) # need
    #     commit(submodule_repo_path, 'Initialized Repository', ' --allow-empty ')
    #     
    #     add_submodule(top_lvl_repo_path, submodule_repo_url)
    #     
    #     add_all(top_lvl_repo_path)
    #     commit_msg = "Initialized repository as submodule:  " + ntpath.basename(submodule_repo_path)
    #     commit(top_lvl_repo_path, commit_msg)
    
    def commit_current_changes_with_commit_meta_data(self, commit, print_output, print_cmd):
        self.add_all_files(print_output, print_cmd)
        self.commit_full(msg = commit.subject + '/n' + commit.body,
                         author = commit.author,
                         date = commit.author_date,
                         print_output = print_output,
                         print_cmd = print_cmd)
        
        print('in Git_Repo, logging commit info of first commit  REMOVE THIS VVVVVVVVVV !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        time.sleep(1)#````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````)
        self.build_commit_l()
        print('out of build_commit_l')
        self.commit_l[-1].log_commit_data("C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\\test_log.txt")
#         
        
        
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Specific Utility Commands - Return
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    
    def get_submodule_path_l(self):
        return self.run_git_cmd("git config --file .gitmodules --get-regexp path | awk '{ print $2 }'", shell = True)
    
    
    def get_num_commits(self):
        return len(self.get_abrv_commit_hash_l())
    
    
    # most recent commit at position 0
    def get_abrv_commit_hash_l (self, print_output = False, print_cmd = False):  
        raw_l = self.run_git_cmd('git log --oneline --pretty=format:"%h"', print_output , print_cmd, decode = True)
        
        if isinstance(raw_l, str):
            raw_l = [raw_l]
        
        
        abrv_commit_hash_l = []
        
        if raw_l != None:
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
            Internal Build / init Functions
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    
    def init_submodule_l(self):
        sm_path_l = self.get_submodule_path_l()
        
        if sm_path_l != None:
            for sm_path in sm_path_l:
                new_sm_repo = Git_Repo(sm_path)
                self.add_as_submodule(new_sm_repo)
    
    
    # takes about 40 sec for ip_repo with no prints
    def build_commit_l(self, limited_load = False): 
        
        if LOAD_COMMIT_L_FROM_JSON_FILE_IF_EXISTS and fsu.is_file(COMMIT_L_LOG_JSON_FILE_PATH):
            print('Loading commit_l from log file:  ', COMMIT_L_LOG_JSON_FILE_PATH, '...')
            self.load_commit_l_from_log()
        else:
            abrv_commit_hash_l = self.get_abrv_commit_hash_l()
    
    
            if limited_load:
                print('Building commit_l - LIMITED LOAD...')
    #                 for abiv_commit_hash in (abrv_commit_hash_l[:4] + abrv_commit_hash_l[-5:]):
                print('in GIT_Repo, len(hash lit)', len(abrv_commit_hash_l))#``````````````````````````````````````````````````````````````````````````````````````````````````````
#                 for abiv_commit_hash in (abrv_commit_hash_l[:2] + [abrv_commit_hash_l[-12]] + [abrv_commit_hash_l[-13]] + abrv_commit_hash_l[-2:]):
                for abiv_commit_hash in (abrv_commit_hash_l[-2:]):
                    c = Git_Commit.Git_Commit(abiv_commit_hash, self.run_git_cmd)
                    self.commit_l.append(c)
                    
            else:
        
                print('Building commit_l normally...')#``````````````````````````````````````````````````````````````````````````````````````````````````````````
                print(' in git repo, building commit_l, abrv_commit_hash_l', abrv_commit_hash_l)#`````````````````````````````````````````````````````````````````
                
                for abiv_commit_hash in abrv_commit_hash_l:
                    c = Git_Commit.Git_Commit(abiv_commit_hash, self.run_git_cmd)
                    self.commit_l.append(c)
        
                print('# of commits in commit_l:  ', len(self.commit_l))#````````````````````````````````````````````````````````````````````````````````````````````````
                
                if LOG_COMMIT_L:
                    print('Logging newly created commit_l to json file:  ', COMMIT_L_LOG_JSON_FILE_PATH, '...')
                    self.log_commit_l()
    
    
    
    
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Log Functions
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
                    
    def log_full_repo_show(self, out_file_path):
        print('  Logging the show output of all commits to:  ', out_file_path, '...')
        txt_logger.write([], out_file_path)
        
        for commit in self.commit_l:
            txt_logger.write('\n----------------------------------------------------------------\n', out_file_path, write_mode = 'append')
            cmd = 'git show --name-only ' + commit.abrv_commit_hash + ' >> ' + out_file_path
    #             cmd = 'git show --name-only ' + commit.abrv_commit_hash
            self.run_git_cmd(cmd, print_output = True, print_cmd = True, shell = True, decode = True)
            
    
    # logs self.commit_l into a json file that can be loaded back in to avoid
    # waiting 40 seconds to build it each time for testing
    def log_commit_l(self):
        log_l = []
        
        for commit in self.commit_l:
            log_l.append(commit.json_log_tup())
            
        json_logger.write(log_l, COMMIT_L_LOG_JSON_FILE_PATH)
        
        
    def load_commit_l_from_log(self):
        commit_data_l = json_logger.read(COMMIT_L_LOG_JSON_FILE_PATH)
        abrv_commit_hash_l = self.get_abrv_commit_hash_l()
        
        if len(abrv_commit_hash_l) != len(commit_data_l):
            raise Exception("ERROR:  len(abrv_commit_hash_l) != len(commit_data_l): ", len(abrv_commit_hash_l), '  !=  ', len(commit_data_l), \
                            ' the number of commits in the repo is different than the number of commits in the log file')
        
        for commit_num, commit_data_tup in enumerate(commit_data_l):
            c = Git_Commit.Git_Commit(abrv_commit_hash_l[commit_num], self.run_git_cmd, commit_data_tup)
    #             c.print_me()#`````````````````````````````````````````````````````````````````````````````````````````````
            self.commit_l.append(c)
    
    
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            General Utility Functions
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    def get_submodule_path_l(self):
        sm_path_l = []
         
        for sm_repo in self.submodule_l:
            sm_path_l.append(sm_repo.path)
             
        return sm_path_l
            
        
            
            
            
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Misc. Testing Functions
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''    
    def print_commit_l_first_and_last(self):
        self.commit_l[0].print_me()
        self.commit_l[-1].print_me()
        print('size of self.commit_l:  ', len(self.commit_l))
        
    
        


#         from submodules.logger import json_logger
#         json_logger.write(self.commit_l, 'test_commit_l.json')
        

#     def init_commit(self, abrv_commit_hash):




# 
# 
# def run_git_cmd(repo_path, cmd, print_output = False, print_cmd = False):
#     cd(repo_path)
#     run_cmd(cmd, print_output, print_cmd)
#     
#     
#     
#     
#     
# def commit(repo_path, msg, options_str = ''):
#     # options_str = ''
#     # for option in option_l:
#         # options_str += ' ' + option + ' '
#         
#     cd(repo_path)
#     cmd = 'git commit ' + options_str + ' -m "' + msg + '"'
#     # cmd_out = subprocess.check_output(cmd, shell = False)
#     # print(cmd_out)
#     
#     run_cmd(cmd, print_output = True)
#     
#     
# def add(repo_path, options_str = ''):
#     cd(repo_path)
#     cmd = 'git add ' + options_str
#     # cmd_out = subprocess.check_output(cmd, shell = False)
#     # print(cmd_out)
#     
#     run_cmd(cmd, print_output = True)
#     
#     
# 
#     
# '''
# # adds and commits all files in existing repo at repo_path with given msg
# def commit_all_files(repo_path, msg):
#     cd(repo_path)
#     cmd = 'git add .'
#     print(subprocess.check_output(cmd, shell = False))
#     
#     cmd = 'git commit -m "' + msg + '"'
#     print(subprocess.check_output(cmd, shell = False))
# '''
#     
# # adds the existing repo at submodule_repo_url as a submodule of the existing repo at top_lvl_repo_path
# # submodule repo must have at least one commit (does not need to have been pushed)
# def add_submodule(top_lvl_repo_path, submodule_repo_url):
#     cd(top_lvl_repo_path)
#     # print('\n  in git_utils, in ' , top_lvl_repo_path, '  ,about to add submodule... \n')#`````````````````````````````````````````````````
#     cmd = 'git submodule add ' + submodule_repo_url
#     # print(cmd)
#     # print(subprocess.check_output(cmd))
#     run_cmd(cmd, print_output = True)
#     
#     
# def add_branch(repo_path, branch_name):
#     cd(repo_path)
#     cmd = 'git branch ' + branch_name
#     run_cmd(cmd, print_output = True, print_cmd = True)
#     
#     
# def checkout_branch(repo_path, branch_name):
#     cd(repo_path)
#     cmd = 'git checkout ' + branch_name
#     run_cmd(cmd, print_output = True, print_cmd = True)
#     
# # merges the branch you are in into branch_name_to_merge_into
# def merge_branch(repo_path, branch_name_to_merge_into, options_str = ''):
#     cd(repo_path)
#     cmd = 'git merge ' + options_str + ' ' + branch_name_to_merge_into
#     run_cmd(cmd, print_output = True, print_cmd = True)
#     
#     
# def tag(repo_path, tag_name):
#     cd(repo_path)
#     cmd = 'git tag ' + tag_name
#     run_cmd(cmd, print_output = True, print_cmd = True)
#     
#     
# def add_all(repo_path):  
#     add(repo_path, ' . ')
#     
# 
#     
#     
# # adds existing, brand new, empty repo as a submodule of existing repo
# def add_new_repo_as_submodule(top_lvl_repo_path, submodule_repo_path, submodule_repo_url):
#     add_all(submodule_repo_path) # need
#     commit(submodule_repo_path, 'Initialized Repository', ' --allow-empty ')
#     
#     add_submodule(top_lvl_repo_path, submodule_repo_url)
#     
#     add_all(top_lvl_repo_path)
#     commit_msg = "Initialized repository as submodule:  " + ntpath.basename(submodule_repo_path)
#     commit(top_lvl_repo_path, commit_msg)
#     
    
    
''' -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV -- All Utilities Standard Footer -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV -- '''
sys.modules = og_sys_modules
''' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ '''
def main():
    import repo_transfer
    repo_transfer.main()
# #     SUBMODULE_REPO_PATH = "C:\\Users\\mt204e\\Documents\    est\\git_test\\repo_from_command_line_test_dir\\ip_test_from_cmd_0\\submodule_repo"
# #     SUBMODULE_REPO_URL = "https://ba-bit.web.boeing.com/users/mt204e/repos/submodule_repo"
# #     TOP_LVL_REPO_PATH = "C:\\Users\\mt204e\\Documents\    est\\git_test\\repo_from_command_line_test_dir\\ip_test_from_cmd_0"
# #     
# #     # commit_all_files(SUBMODULE_REPO_PATH, 'Initialized Repository')
# #     # add_submodule(TOP_LVL_REPO_PATH, SUBMODULE_REPO_URL)
# #     
# #     add_new_repo_as_submodule(TOP_LVL_REPO_PATH, SUBMODULE_REPO_PATH, SUBMODULE_REPO_URL)
# #     
# 
#     g = Git_Repo("C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\\ip_repo")
# #     g.run_git_cmd('git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n H   commit hash: ', print_output = True, print_cmd = True)
#     g.build_commit_l(limited_load = True)
#     
# #     print(g.commit_l[-1].subject)
#     g.print_commit_l_first_and_last()
# #     g.run_git_cmd('git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n H   commit hash: ', print_output = True, print_cmd = True, run_type = "call")
#     
# #     g.run_git_cmd('git log 34f2fab -n1 --oneline > C:\Users\mt204e\Documents\projects\Bitbucket_repo_setup\svn_to_git_ip_repo    est_log.txt')
# #     import subprocess
# #     cd(g.path)
# #     
# # #     p = subprocess.Popen(['git', 'log',  '34f2fab',  '-n1',  '--oneline ', ' > ',  "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\    est_log.txt"])
# #     
# # #     subprocess.call('git log 34f2fab -n1 --oneline --pretty=format:"COMMIT_HASH:%h  BODY: %b  COMMIT_NOTES: %n SUBJECT: %s  AUTHOR_DATE: %ad" > "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\    est_log.txt"' , shell = True)
# #     su.run_cmd('git log 34f2fab -n1 --oneline --pretty=format:"COMMIT_HASH:%h  BODY: %b  COMMIT_NOTES: %n SUBJECT: %s  AUTHOR_DATE: %ad" > "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\    est_log.txt"', shell=True )
# # 
# # #     print('git log 34f2fab -n1 --oneline --pretty=format:"COMMIT_HASH: %h\n  BODY: %b\n  COMMIT_NOTES: %n SUBJECT: %s  AUTHOR_DATE: %ad" > C:\Users\mt204e\Documents\projects\Bitbucket_repo_setup\svn_to_git_ip_repo    est_log.txt')
# # #     import os
# # #     os.system('git log 34f2fab -n1 --oneline --pretty=format:"COMMIT_HASH:\n\n\n %h  BODY: %b  COMMIT_NOTES: %n SUBJECT: %s  AUTHOR_DATE: %ad" > "C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\    est_log.txt"' )
# #     
    
    
if __name__ == '__main__':
    import repo_transfer
    repo_transfer.main()
    

#     r = Git_Repo("C:\\Users\\mt204e\\Documents\    est\\git_test\    r0")
#     print(r.exists())
#     
#     r = Git_Repo("C:\\Users\\mt204e\\Documents\    est")
#     print(r.exists())

#     main()
    
    # git commit --allow-empty -m "manual first commit from cmd line"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    