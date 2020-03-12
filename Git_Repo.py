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
         
        self.flow_init__manual_flag = False # set true by flow_init_default(), will not detect if git flow is initialized elsewhere
     
        if remote_base_url != None:
            self.url = remote_base_url + '//' + self.name
         
        self.init_submodule_l()
         
         
         
    def run_git_cmd(self, cmd, print_output = False, print_cmd = False, sleep = 0, shell = False, run_type = 'popen', decode = False, strip = False, always_output_list = False):
    #         if run_type not in ['popen']
        eu.error_if_param_key_not_in_whitelist(run_type, ['popen', 'call'])
         
        og_cwd = os.getcwd()
        cd(self.path)
         
        if run_type == 'popen':
            output = su.run_cmd_popen(cmd, print_output, print_cmd, shell, decode, strip, always_output_list)
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
     
    def add_all_files     (self, print_output = False, print_cmd = False):  self.run_git_cmd('git add .'          , print_output
                                                                                                                  , print_cmd)
    def push_all_branches (self, print_output = False, print_cmd = False):  self.run_git_cmd('git push --all'     , print_output
                                                                                                                  , print_cmd)
    def undo_checkout     (self, print_output = False, print_cmd = False):  self.run_git_cmd('git switch -'       , print_output
                                                                                                                  , print_cmd)    
    def init_repo_simple  (self, print_output = False, print_cmd = False):  
                                                                            fsu.make_dir_if_not_exist(self.path)
                                                                            self.run_git_cmd('git init'           , print_output
                                                                                                                  , print_cmd)   
                             
     
    def flow_init_default (self, print_output = False, print_cmd = False):  
                                                                            self.run_git_cmd('git flow init -d -f', print_output
                                                                                                                  , print_cmd)
                                                                            self.flow_init__manual_flag = True
     
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Basic Commands - One Arg
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
     
    def commit_simple           (self, msg         , print_output = False, print_cmd = False):  self.run_git_cmd('git commit -a -m "' + msg + '"'       , print_output
                                                                                                                                                        , print_cmd)
    def checkout_simple         (self, branch_name , print_output = False, print_cmd = False):  self.run_git_cmd('git checkout ' + branch_name          , print_output
                                                                                                                                                        , print_cmd)
    def make_branch_and_checkout(self, branch_name , print_output = False, print_cmd = False):  self.run_git_cmd('git checkout -b ' + branch_name       , print_output
                                                                                                                                                        , print_cmd)
    # adds repo at the given URL as a submodule of this repo
    def add_submodule_simple    (self, repo_url    , print_output = False, print_cmd = False):  self.run_git_cmd('git submodule add' + repo_url         , print_output
                                                                                                                                                        , print_cmd)
    def flow_release_start      (self, version_str , print_output = False, print_cmd = False):  self.run_git_cmd('git flow release start ' + version_str, print_output
                                                                                                                                                        , print_cmd)
    def delete_tag              (self, tag_name    , print_output = False, print_cmd = False):  self.run_git_cmd('git tag -d ' + tag_name               , print_output
                                                                                                                                                        , print_cmd)
    # merges given branch name into current branch without fast-forwarding 
    def merge_no_ff             (self, branch_name , print_output = False, print_cmd = False):  self.run_git_cmd('git merge --no-ff ' + branch_name     , print_output
                                                                                                                                                        , print_cmd
                                                                                                                                                        , sleep = 0.5) # not optimized    
 
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Basic Commands - Many Args
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''  
         
    # remote name should be something like "origin"        
    def add_remote          (self, remote_name, remote_url, print_output = False, print_cmd = False):  self.run_git_cmd('git remote add ' + remote_name + ' ' + remote_url , print_output
                                                                                                                                                                           , print_cmd)
    # adds tag on current head commit
    def add_tag_simple      (self, tag_name, tag_msg      , print_output = False, print_cmd = False):  self.run_git_cmd('git tag -a ' + tag_name + ' -m ' + tag_msg        , print_output
                                                                                                                                                                           , print_cmd)
    
    def flow_release_finish (self, version_str, tag_msg   , print_output = False, print_cmd = False):  
        self.run_git_cmd("git flow release finish '" + version_str + "' -m " + '"' + tag_msg + '"'          , print_output, print_cmd)
        self.checkout_simple('develop') # just in case this is this first commit?
     
         
    def commit_full(self, subject, body, author, date, committer_name, committer_email, committer_date, print_output = False, print_cmd = False):  
 
        self.run_git_cmd('cmd /v /c "set GIT_COMMITTER_DATE=' + committer_date + '&&'
                                     + ' git -c user.name="'  + committer_name  + '"'
                                     + ' -c user.email="'     + committer_email + '"'
                                     + ' commit '
                                     + ' --date="'            + date            + '"'
                                     + ' -m "'                + subject         + '"'
                                     + ' -m "'                + body            + '"'
                                     , print_output, print_cmd)
        
    def merge_full(self, branch_name, committer_name, committer_email, committer_date, print_output = False, print_cmd = False):
#         self.run_git_cmd('cmd /v /c "set GIT_COMMITTER_DATE=' + committer_date + '&&'
#                                      + ' git -c user.name="'  + committer_name  + '"'
#                                      + ' -c user.email="'     + committer_email + '"'
#                                      + ' merge --no-ff '      + branch_name,
#                                      print_output, print_cmd)

        

        self.run_git_cmd('git config user.name "John Doe"')

        self.run_git_cmd('cmd /v /c "set GIT_COMMITTER_DATE=' + committer_date + '&&'
                                     + ' git merge --no-ff '      + branch_name,
                                     print_output, print_cmd)
 
     
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
   
    def get_full_hash_of_tagged_commit(self, tag_name, print_output = False, print_cmd = False):    return self.run_git_cmd('git show-ref -s ' + tag_name            , print_output, print_cmd, decode = True, strip = True)
    
    def get_abrv_hash_of_head_commit  (self          , print_output = False, print_cmd = False):    return self.run_git_cmd('git log --pretty=format:%h -n 1'        , print_output, print_cmd, decode = True, strip = True)

     
    def get_submodule_path_l(self):
        return self.run_git_cmd("git config --file .gitmodules --get-regexp path | awk '{ print $2 }'", shell = True)    
    
    def get_containing_branches_of_commit_hash(self, commit_hash, print_output = False, print_cmd = False):
        return self.run_git_cmd('git branch --contains ' + commit_hash   , print_output, print_cmd, decode = True, strip = True, always_output_list = True)
    
    
    def get_branch_l(self, print_output = False, print_cmd = False):
        return self.run_git_cmd('git branch', print_output, print_cmd, decode = True, strip = True, always_output_list = True)
     
     
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
     
     
    def get_tag_l(self, print_output = False, print_cmd = False):
        cmd = 'git tag'
        tag_l = self.run_git_cmd(cmd, print_output, print_cmd, decode = True, strip = True)
        
        if tag_l == None:
            return []
        return tag_l
    
    def head_on_support_branch(self, print_output = False, print_cmd = False):
        head_abrv_hash = self.get_abrv_hash_of_head_commit(print_output, print_cmd)
        containing_branches = self.get_containing_branches_of_commit_hash(head_abrv_hash, print_output = True, print_cmd = True)
        return 'support' in containing_branches[0]

             
     
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
#                 for abiv_commit_hash in (abrv_commit_hash_l[-2:]):
#                 for abiv_commit_hash in (abrv_commit_hash_l[-12::-14]):
#                 for abiv_commit_hash in ([abrv_commit_hash_l[-12]] + [abrv_commit_hash_l[-13]]): # axi global regs changes only
#                 for abiv_commit_hash in ([abrv_commit_hash_l[-18]] + [abrv_commit_hash_l[-16]] + abrv_commit_hash_l[-8:-4]): # axi_MinIM_1.1 -> 1.2
#                 for abiv_commit_hash in ([abrv_commit_hash_l[-116]] + [abrv_commit_hash_l[-18]] + [abrv_commit_hash_l[-15]]): # axi_dma out of order versions
                for abiv_commit_hash in (abrv_commit_hash_l[-32:]): # axi_dma up to v1.4
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
         


''' -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV -- All Utilities Standard Footer -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV -- '''
sys.modules = og_sys_modules
''' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ '''
if __name__ == '__main__':
    import repo_transfer
    repo_transfer.main()

#     print_output = True
#     print_cmd = True
#         
#     r = Git_Repo('C:\\Users\\mt204e\\Documents\\test\\git_test\\git_flow_test')
#     print(r.get_tag_l(print_output, print_cmd))
       
   
#     r = Git_Repo("C:\\Users\\mt204e\\Documents\    est\\git_test\    r0")
#     print(r.exists())
#     
#     r = Git_Repo("C:\\Users\\mt204e\\Documents\    est")
#     print(r.exists())
   
#     main()
       
    # git commit --allow-empty -m "manual first commit from cmd line"
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       