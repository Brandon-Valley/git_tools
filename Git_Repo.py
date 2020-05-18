import ntpath
import time
import os


if __name__ == "__main__": 
    from   usms.logger            import json_logger
    from   usms.logger            import txt_logger    
    from   usms.file_system_utils import file_system_utils as fsu
    from   usms.subprocess_utils  import subprocess_utils  as su
    import                               Git_Commit
else:
    from . usms.logger            import json_logger
    from . usms.logger            import txt_logger    
    from . usms.file_system_utils import file_system_utils as fsu
    from . usms.subprocess_utils  import subprocess_utils  as su
    from .                        import Git_Commit

    
    
COMMIT_L_LOG_JSON_FILE_PATH = 'commit_l.json'
LOAD_COMMIT_L_FROM_JSON_FILE_IF_EXISTS = False
LOG_COMMIT_L = False

    
     
def cd(dir_path):
    
#     while(True):
#         try:
#             os.chdir(dir_path)
#             break
#         except:
#             print('got permission error when trying to cd, trying again...')
    
    os.chdir(dir_path)
     
     
class Git_Repo:
    def __init__(self, repo_path, remote_base_url = None):
        self.path        = repo_path
        self.name        = ntpath.basename(self.path)
        self.commit_l    = []
        self.url         = None
        
#         self.submodule_l = [] # manually updated
         
        self.flow_init__manual_flag = False # set true by flow_init_default(), will not detect if git flow is initialized elsewhere
     
        if remote_base_url != None:
            self.url = remote_base_url + '//' + self.name
         
#         self.init_submodule_l()
         
         
         
    def run_git_cmd(self, cmd, print_output = False, print_cmd = False, sleep = 0, shell = False, run_type = 'popen', decode = False, strip = False, always_output_list = False, return_stderr = True):
    #         if run_type not in ['popen']
        if run_type not in ['popen', 'call']:
            raise Exception("ERROR: run type must be one of " + str(['popen', 'call'] + ' got: ' + str(run_type)))
         
        og_cwd = os.getcwd()
        cd(self.path)
         
        if run_type == 'popen':
            output = su.run_cmd_popen(cmd, print_output, print_cmd, shell, decode, strip, always_output_list, return_stderr = return_stderr)
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
     
    def add_all_files     (self, print_output = False, print_cmd = False):  self.run_git_cmd('git add .'            , print_output
                                                                                                                    , print_cmd)
    def deep_clean        (self, print_output = False, print_cmd = False):  self.run_git_cmd('git clean -ffxd'      , print_output
                                                                                                                    , print_cmd)
    def update_submodules (self, print_output = False, print_cmd = False):  self.run_git_cmd('git submodule update --init --recursive'      , print_output
                                                                                                                                            , print_cmd)    
    def push_all_branches (self, print_output = False, print_cmd = False, **kwargs): return self.run_git_cmd('git push --all' , print_output
                                                                                                                        , print_cmd, **kwargs)
    def undo_checkout     (self, print_output = False, print_cmd = False):  self.run_git_cmd('git switch -'         , print_output
                                                                                                                    , print_cmd)    
    def init_repo_simple  (self, print_output = False, print_cmd = False):                                          
                                                                            fsu.make_dir_if_not_exist(self.path)    
                                                                            self.run_git_cmd('git init'             , print_output
                                                                                                                    , print_cmd)   
                                                                                                                    
    def flow_init_default (self, print_output = False, print_cmd = False):                                          
                                                                            self.run_git_cmd('git flow init -d -f'  , print_output
                                                                                                                    , print_cmd)
                                                                            self.flow_init__manual_flag = True
#     # makes and checks out master and develop, dosn't take forever                                                                                                                                                                                            
#     def pretend_to_init_git_flow (self, print_output = False, print_cmd = False):                                          
#                                                                             self.run_git_cmd('git checkout -b master'  , print_output
#                                                                                                                         , print_cmd)
#                                                                             self.run_git_cmd('git checkout -b develop'  , print_output
#                                                                                                                         , print_cmd)
#                                                                             self.flow_init__manual_flag = True
                                                                                  
    def undo_cherry_pick  (self, print_output = False, print_cmd = False):                                          
                                                                            self.run_git_cmd('git reset'            , print_output
                                                                                                                    , print_cmd)
                                                                            self.run_git_cmd('git clean -dfx'       , print_output
                                                                                                                    , print_cmd) 
                                                                              
    def clone_to_cwd      (self, print_output = False, print_cmd = False, shell = False, run_type = 'popen'):  
        # just running make_dir_if_not_exist() before clone still sometimes throws FileNotFoundError
        try:
            self.run_git_cmd('git clone ' + self.url + ' . ', print_output, print_cmd, shell, run_type)  
        except FileNotFoundError:
            fsu.make_dir_if_not_exist(self.path) 
            self.run_git_cmd('git clone ' + self.url + ' . ', print_output, print_cmd, shell, run_type) 
            
             
#     def track_all_remote_branches(self, print_output = False, print_cmd = False, run_type = 'popen'): 
    def track_all_remote_branches(self, **kwargs): 
#         cmd = 'for /f "delims=" %%r in (' + "'git branch -r ^| grep -v master') do git checkout --track %%r"
        cmd = 'for /f "delims=" %r in (' + "'git branch -r ^| grep -v master') do git checkout --track %r"
#         self.run_git_cmd(cmd, print_output, print_cmd, return_stderr = False, shell = True, run_type = run_type)       
        self.run_git_cmd(cmd, return_stderr = False, shell = True, **kwargs)       
              
    def delete_lock_file (self):
        fsu.delete_if_exists(self.path + '//.git//index.lock')
    
                                                                               
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Basic Commands - One Arg
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
     

    def checkout_simple         (self, branch_name        , print_output = False, print_cmd = False):  self.run_git_cmd('git checkout ' + branch_name           , print_output
                                                                                                                                                                , print_cmd)
    def make_branch_and_checkout(self, branch_name        , print_output = False, print_cmd = False):  self.run_git_cmd('git checkout -b ' + branch_name        , print_output
                                                                                                                                                                , print_cmd)
    def flow_release_start      (self, version_str        , print_output = False, print_cmd = False):  self.run_git_cmd('git flow release start ' + version_str , print_output
                                                                                                                                                                , print_cmd)
    def delete_tag              (self, tag_name           , print_output = False, print_cmd = False):  self.run_git_cmd('git tag -d ' + tag_name                , print_output
                                                                                                                                                                , print_cmd)
    # merges given branch name into current branch without fast-forwarding 
    def merge_no_ff             (self, branch_name        , print_output = False, print_cmd = False):  self.run_git_cmd('git merge --no-ff ' + branch_name      , print_output
                                                                                                                                                                , print_cmd
                                                                                                                                                                , sleep = 0.5) # not optimized  
    def remove_submodule        (self, submodule_rel_path , print_output = False, print_cmd = False):  
                                                                                                    self.run_git_cmd('git rm '              + submodule_rel_path, print_output , print_cmd)
                                                                                                    self.run_git_cmd('rm -rf .git/modules/' + submodule_rel_path, print_output , print_cmd)
     
 
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Basic Commands - Many Args
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''  
    def commit_simple           (self, msg, options_str = ''              , print_output = False, print_cmd = False, **kwargs):  self.run_git_cmd('git commit -a ' + options_str + ' -m "' + msg + '"' , print_output
                                                                                                                                                                                                   , print_cmd, **kwargs)     
         
    # remote name should be something like "origin"        
    def add_remote          (self, remote_name, remote_url            , print_output = False, print_cmd = False):  self.run_git_cmd('git remote add ' + remote_name + ' ' + remote_url             , print_output
                                                                                                                                                                                                   , print_cmd)
    
    # adds tag on current head commit unless given hash in options str
    def add_tag_simple      (self, tag_name, tag_msg, options_str = '', print_output = False, print_cmd = False):  self.run_git_cmd('git tag -a ' + tag_name + ' -m ' + tag_msg + ' ' + options_str, print_output
                                                                                                                                                                                                   , print_cmd)
    # adds repo at the given URL as a submodule of this repo                                                                                                                  
    def add_submodule_simple    (self, repo_url, repo_path, options_str = '', print_output = False, print_cmd = False):
                                self.run_git_cmd('git submodule add ' + repo_url + ' ' + repo_path + ' ' + options_str , print_output
                                                                                                                                                                           , print_cmd)
#                                 self.init_submodule_l()
    
    def flow_release_finish (self, version_str, tag_msg   , print_output = False, print_cmd = False):  
        self.run_git_cmd("git flow release finish '" + version_str + "' -m " + '"' + tag_msg + '"'          , print_output, print_cmd)
        self.checkout_simple('develop') # just in case this is this first commit?
     
         
#     def commit_full(self, subject, body, author, date, committer_name, committer_email, committer_date, options_str = '', print_output = False, print_cmd = False):  
    def commit_full(self, msg_file_path, author, date, committer_name, committer_email, committer_date, options_str = '', print_output = False, print_cmd = False):  
#         print('in Git_Repo, body: ', body)#```````````````````````````````````````````````````````````````````````````````````````````
#  
#         cmd =   'cmd /v /c "set GIT_COMMITTER_DATE=' + committer_date  + '&&' \
#         + ' git -c user.name="'  + committer_name             + '"'           \
#         + ' -c user.email="'     + committer_email            + '"'           \
#         + ' commit '                                                          \
#         + ' '                    + options_str                                \
#         + ' --date="'            + date                        + '"'          \
#         + ' -m "'                + subject                     + '"'          \
#         + ' -m "'                + body                        + '"'

#         print('in Git_Repo, body: ', body)#```````````````````````````````````````````````````````````````````````````````````````````
 
        cmd =   'cmd /v /c "set GIT_COMMITTER_DATE=' + committer_date  + '&&' \
        + ' git -c user.name="'  + committer_name             + '"'           \
        + ' -c user.email="'     + committer_email            + '"'           \
        + ' commit '                                                          \
        + ' '                    + options_str                                \
        + ' --date="'            + date                        + '"'          \
        + ' -F "'                + msg_file_path               + '"'           


              
        print('in Git_Repo, cmd:  ', cmd)#```````````````````````````````````````````````````````````````````````````````````````````````````````
        return self.run_git_cmd(cmd, print_output, print_cmd, decode = True, strip = True, always_output_list = True)

        
    def amend_head_commit_date_full(self, new_date_str, committer_name, committer_email, committer_date, print_output = False, print_cmd = False):  
 
        self.run_git_cmd('cmd /v /c "set GIT_COMMITTER_DATE=' + committer_date  + '&&'
                                     + ' git -c user.name="'  + committer_name  + '"'
                                     + ' -c user.email="'     + committer_email + '"'
                                     + ' commit --no-edit --amend '
                                     + ' --date="'            + new_date_str    + '"'
                                     , print_output, print_cmd)
        
        
    def merge_full(self, branch_name, committer_name, committer_email, committer_date, print_output = False, print_cmd = False):
        self.run_git_cmd('cmd /v /c "set GIT_COMMITTER_DATE=' + committer_date  + '&&'
                                     + 'set GIT_AUTHOR_DATE=' + committer_date  + '&&'
                                     + ' git -c user.name="'  + committer_name  + '"'
                                     + ' -c user.email="'     + committer_email + '"'
                                     + ' merge --no-ff '      + branch_name     + '"',
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
    
    
    def get_head_commit               (self          , print_output = False, print_cmd = False):
        head_commit_hash = self.run_git_cmd('git log --pretty=format:%h -n 1'        , print_output, print_cmd, decode = True, strip = True)
        return Git_Commit.Git_Commit(head_commit_hash, self.run_git_cmd)
        

    def get_submodule_path_l(self):
        return self.run_git_cmd("git config --file .gitmodules --get-regexp path | awk '{ print $2 }'", shell = True, decode = True, strip = True, always_output_list = True)  
    
    def get_submodule_name_l(self):
        sm_path_l = self.get_submodule_path_l()
        
        sm_name_l = []
        for sm_path in sm_path_l:
            sm_name_l.append(fsu.get_basename_from_path(sm_path))
        return sm_name_l  
    
    def get_containing_branches_of_commit_hash(self, commit_hash, print_output = False, print_cmd = False):
        return self.run_git_cmd('git branch --contains ' + commit_hash   , print_output, print_cmd, decode = True, strip = True, always_output_list = True)
    
    
    def get_branch_l(self, trimmed = False, print_output = False, print_cmd = False, **kwargs):
        branch_l_raw = self.run_git_cmd('git branch', print_output, print_cmd, decode = True, strip = True, always_output_list = True, **kwargs)
        
        if trimmed == False:
            return branch_l_raw
        else:
            branch_l_trimmed = []
            for branch_str in branch_l_raw:
                branch_l_trimmed.append(branch_str.replace('* ', ''))
            
            return branch_l_trimmed
    

     
     
    def get_num_commits(self, **kwargs):
        return len(self.get_abrv_commit_hash_l(**kwargs))
    

     
    # most recent commit at position 0
    def get_abrv_commit_hash_l (self, print_output = False, print_cmd = False, **kwargs):  
        raw_l = self.run_git_cmd('git log --oneline --pretty=format:"%h"', print_output, print_cmd, decode = True, **kwargs)
                
#         raw_l = self.run_git_cmd('git log --oneline --pretty=format:"%h"', False , print_cmd, decode = True)
         
        if isinstance(raw_l, str):
            if ' does not have any commits yet' in raw_l:
                return []
            else:
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
        print('in Git Repo in head_on_support_branch, containing_branches: ', containing_branches)#````````````````````````````````````````````````````````````````````````````````````````````````
        
        for branch_str in containing_branches:
            if 'support' in branch_str:
                return True
            
        return False
    
    
    def get_commit_from_hash(self, commit_hash):
        return Git_Commit.Git_Commit(commit_hash, self.run_git_cmd)
        
             
     
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Internal Build / init Functions
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
     
    # need????????????????????????????????????????????????????????????????????????????????????????????????????
    def init_submodule_l(self):
        sm_path_l = self.get_submodule_path_l()
         
        if sm_path_l != None:
            for sm_path in sm_path_l:
                new_sm_repo = Git_Repo(sm_path)
                self.add_as_submodule(new_sm_repo)
     
     
    # takes about 40 sec for ip_repo with no prints
    def build_commit_l(self, limited_load = False, repo_hash_svn_id_log_path = None): 
         
        if LOAD_COMMIT_L_FROM_JSON_FILE_IF_EXISTS and fsu.is_file(COMMIT_L_LOG_JSON_FILE_PATH):
            print('Loading commit_l from log file:  ', COMMIT_L_LOG_JSON_FILE_PATH, '...')
            self.load_commit_l_from_log()
        else:
            # this part really shouldn't be in this submodule, but I'm lazy
            abrv_commit_hash_l = self.get_abrv_commit_hash_l()
     
#             print('abrv_commit_hash_l:  ', abrv_commit_hash_l)#`1```````````````````````````````````````````````````````````````````
     
            if limited_load:
                
                print('Building commit_l - LIMITED LOAD...')
                print('in GIT_Repo, len(hash lit)', len(abrv_commit_hash_l), ' <-- if this number is not 322, 359, or 293, probably means ip repo messed up')#``````````````````````````````````````````````````````````````````````````````````````````````````````
                if not (len(abrv_commit_hash_l) == 322 or len(abrv_commit_hash_l) == 293 or len(abrv_commit_hash_l) == 359):
                    raise Exception("^^^ IP repo probably messed up")

                
#                 svn_rev_l = [1142, 1141, 1131, 1130, 1128, 980]  # Fast_Enet_Support
#                 svn_rev_l = [1161, 930]  # axi4lite_LTC2666 / adding empty commit
#                 svn_rev_l = [1160, 930]  # axi4lite_LTC2666 / removing projects as submodules
#                 svn_rev_l = [732, 295]  # vv_index.xml / other files in src_ip_repo (there are no other files)
#                 svn_rev_l = [35, 31]  # axi_MinIM 
#                 svn_rev_l = [49]  # 
#                 svn_rev_l = [1155, 1154, 1153, 1152, 1151, 1150, 1149,1126, 1020]  # AXI_HI_84...
#                 svn_rev_l = [1125, 1020]  # AXI_HI_84...
#                 svn_rev_l = [158, 94, 65]  # axi_MinIM duplicate commit merge bug
#                 svn_rev_l = [920]  # double quotes in commit msg
#                 svn_rev_l = [953]  # multi-line commit msg
#                 svn_rev_l = [931, 930]  # axi4lite
#                 svn_rev_l = [50, 49, 30]  # axi_global_regs
#                 svn_rev_l = [1161]  # empty commit - Rich told me
#                 svn_rev_l = [976, 158, 94, 65, 60,  44, 7]  # axi_dma not making support branch when tagging after commit for 1.1 + axi_dm_uart
#                 svn_rev_l = [976, 893, 887, 7]  # axi_dma, axi_adis1647x short
#                 svn_rev_l = [977, 976, 893, 887, 7]  # axi_dma, axi_uart short
#                 svn_rev_l = [976, 887, 309, 308, 158, 94, 65, 63, 60,  44, 7]  # axi_dma full
                svn_rev_l = [977, 976, 887, 309, 308, 158, 94, 65, 63, 60,  44, 7]  # axi_dma full + axi_dm_uart
#                 svn_rev_l = [967, 736]
#                 svn_rev_l = [851, 822, 427, 378, 294, 286, 107 ] # axi_hx1_spi tagging 1.2 bug
                import repo_transfer
                       
                commit_num_svn_id_d = json_logger.read(repo_transfer.COMMIT_NUM_SVN_ID_JSON_PATH)
                       
                limited_abrv_commit_hash_l = []
                for svn_rev_num in svn_rev_l:
                    commit_num = commit_num_svn_id_d[str(svn_rev_num)]
                    print('Limited Load, loading commit #: ', commit_num, "   DO NOT DELETE THIS PRINT") # stuff breaks if you remove this, no clue why
                    abrv_commit_hash = abrv_commit_hash_l[commit_num]
                    limited_abrv_commit_hash_l.append(abrv_commit_hash)
                           
#                 print(limited_abrv_commit_hash_l)
#                 wait() 
       
                for abiv_commit_hash in limited_abrv_commit_hash_l: 
                    c = Git_Commit.Git_Commit(abiv_commit_hash, self.run_git_cmd)
                    self.commit_l.append(c)

                
                
#     #                 for abiv_commit_hash in (abrv_commit_hash_l[:4] + abrv_commit_hash_l[-5:]):
# #                 for abiv_commit_hash in (abrv_commit_hash_l[:2] + [abrv_commit_hash_l[-12]] + [abrv_commit_hash_l[-13]] + abrv_commit_hash_l[-2:]):
# #                 for abiv_commit_hash in (abrv_commit_hash_l[-2:]):
# #                 for abiv_commit_hash in (abrv_commit_hash_l[-12::-14]):
# #                 for abiv_commit_hash in ([abrv_commit_hash_l[-12]] + [abrv_commit_hash_l[-13]]): # axi global regs changes only
# #                 for abiv_commit_hash in ([abrv_commit_hash_l[-18]] + [abrv_commit_hash_l[-16]] + abrv_commit_hash_l[-8:-4]): # axi_MinIM_1.1 -> 1.2
# #                 for abiv_commit_hash in ([abrv_commit_hash_l[-116]] + [abrv_commit_hash_l[-18]] + [abrv_commit_hash_l[-15]]): # axi_dma out of order versions
# #                 for abiv_commit_hash in (abrv_commit_hash_l[-32:]): # axi_dma up to v1.4
# #                 for abiv_commit_hash in (abrv_commit_hash_l[-22:]): # axi_uart
# #                 for abiv_commit_hash in (abrv_commit_hash_l[5:34]): # AXI_HI_8429
# #                 for abiv_commit_hash in ([abrv_commit_hash_l[59]]): # golden .ZIP - well formatted, spaced out multi-line comment
# #                 for abiv_commit_hash in (abrv_commit_hash_l[-22:]): # fresh pull after axi_dma_sdlc_v0_6
# #                 for abiv_commit_hash in (abrv_commit_hash_l[239:]): # add_branch_ip ,<<<===================================================<<<===<<<===<<<===<<<===<<<===<<<===<<<===<<<
#                 for abiv_commit_hash in (abrv_commit_hash_l[-18:]): # 
#                     c = Git_Commit.Git_Commit(abiv_commit_hash, self.run_git_cmd)
#                     self.commit_l.append(c)
                      
            else:
          
                print('Building commit_l normally...')#``````````````````````````````````````````````````````````````````````````````````````````````````````````
#                 print(' in git repo, building commit_l, abrv_commit_hash_l', abrv_commit_hash_l)#`````````````````````````````````````````````````````````````````
                  
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
     
     
#     ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
#     '''                                                                           
#             General Utility Functions
#     '''
#     ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
#     def get_submodule_path_l(self):
#         sm_path_l = []
#           
#         for sm_repo in self.submodule_l:
#             sm_path_l.append(sm_repo.path)
#               
#         return sm_path_l
             
         
             
             
             
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Misc. Testing Functions
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''    
    def print_commit_l_first_and_last(self):
        self.commit_l[0].print_me()
        self.commit_l[-1].print_me()
        print('size of self.commit_l:  ', len(self.commit_l))
         



if __name__ == '__main__':
#     import repo_transfer
#     repo_transfer.main()
# 
#     import add_branch_ip
#     add_branch_ip.main()

    from PIC_transfer import PIC_transfer
    PIC_transfer.main()

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
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       