if __name__ == "__main__": 
    import        commit_log_format_strings as clfs
else:
    from . import commit_log_format_strings as clfs



VAR_DELIM = '__$$@-VAR_DELIM-@$__'



class Git_Commit:
    # run_git_cmd will execute the given command inside the repo that initialized the Git_Commit class
    def __init__(self, abbreviated_commit_hash, run_git_cmd, data_tup = None):
        self.run_git_cmd      = run_git_cmd
        self.abrv_commit_hash = abbreviated_commit_hash
        
        self.author           = None
        self.author_email     = None
        self.author_date      = None
        self.subject          = None
        self.body             = None
                           
        self.changed_files_l  = []
        
        self.svn_rev_num      = None
        
        
        # if given data_tup from json log file, load vars from that,
        # otherwise, build commit normally
        if data_tup != None:
            self.load_from_log_data(data_tup)
        else:
        
        
    #         self.log_commit_data('C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\bitbucket_repo_setup_scripts\\test__commit_log.txt')
            
    #         self.run_git_cmd('git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n H   commit hash: ', print_output = True, print_cmd = True) 
    
            # build and run cmd to extract commit info
            cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:"' + VAR_DELIM + clfs.AUTHOR_NAME \
                                                                                          + VAR_DELIM + clfs.AUTHOR_EMAIL \
                                                                                          + VAR_DELIM + clfs.AUTHOR_DATE \
                                                                                          + VAR_DELIM + clfs.SUBJECT     \
                                                                                          + VAR_DELIM + clfs.BODY        \
                                                                                    + '"'
#             print('in Git Commit, cmd:  ', cmd)#```````````````````````````````````````````````````````````````````````````````````````````````
                                                                                           
            raw_commit_data = self.run_git_cmd(cmd     , decode = True, print_output = False, print_cmd = False)
            
            if type(raw_commit_data) == list: # if someone used newlines in their commit body
                raw_commit_data = ''.join(raw_commit_data)
                
#             print('in Git_Commit:  raw_commit_data: ', raw_commit_data)#``````````````````````````````````````````````````````````````````````````````````````````````````````````
            commit_data_l = raw_commit_data.split(VAR_DELIM)
            
#             for e in commit_data_l:#```````````````````````````````````````````````````````````````````````````````````
#                 print(e)
#             print(commit_data_l)#``````````````````````````````````````````````````````````````````````````````````````````````
            
            commit_data_l.pop(0) # remove first empty element
    
            self.author       = commit_data_l.pop(0)                                          
            self.author_email = commit_data_l.pop(0)                                          
            self.author_date  = commit_data_l.pop(0) 
#             print('in Git_Commit, subject portion of raw_commit_data:  ', commit_data_l[0])#`````````````````````````````````````````````````````````````                                 
                                         
            self.subject      = commit_data_l.pop(0)         
#             print('in Git_Commit, body portion of raw_commit_data:  ', commit_data_l[0])#`````````````````````````````````````````````````````````````                                 
            self.body         = commit_data_l.pop(0)  
            
            
            
            # fill self.changed_files_l
            cmd = 'git show --name-only ' + self.abrv_commit_hash
            raw_commit_data_l = self.run_git_cmd(cmd     , decode = True)
     
#             print(raw_commit_data_l)#``````````````````````````````````````````````````````````````````````````````````````````````
#             print(raw_commit_data_l[1])#`````````````````````````````````````````````````````````````````````````````````````````````
            
            
             
            for line in reversed(raw_commit_data_l):
                if line[0] == '\n' or line.startswith('   '):
                    break
                 
                self.changed_files_l.append(line[:-1]) # trim newline
                             
            self.changed_files_l = list(reversed(self.changed_files_l)) # put back in abc order
                     
                     
#             if self.abrv_commit_hash == '0c6a850':#``````````````````````````````````````````````````````````````````````````````````
#                 print('b')
                                                                                              
            # if this commit is from a git repo created by converting from an svn repo
            if 'git-svn-id: ' in self.body:
#                 print('in Git_Commit, self.body: ', self.body)#````````````````````````````````````````````````````````````````````````
                try:
                    self.svn_rev_num = self.body.split(' ')[-2].split('@')[1]
                except IndexError:
                    self.svn_rev_num = self.body.split('git-svn-id: https://wpns04.stl.mo.boeing.com/ANPsvn/Trunk/ip_repo@')[1].split(' ')[0]
            elif 'git-svn-id: ' in self.subject:
                self.svn_rev_num = self.subject.split(' ')[-2].split('@')[1]
                
       
        


    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Commands
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    # undo with git switch -
    def checkout(self, options_str = '', return_stderr = True):
        return self.run_git_cmd('git checkout ' + self.abrv_commit_hash + ' ' + options_str , print_output = True, print_cmd = True, decode = True, strip = True, always_output_list = True, return_stderr = return_stderr)
    
    def cherry_pick(self, options_str = ''):
        return self.run_git_cmd('git cherry-pick ' + self.abrv_commit_hash + ' ' + options_str , print_output = True, print_cmd = True, decode = True, strip = True, always_output_list = True)
    
    
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Get Info
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    def no_changed_files(self):
        return len(self.changed_files_l) == 0
        
    
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Json Log Functions - For Testing
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
        
    # if no log_file_path is given, will log to default location
    def log_commit_data(self, log_file_path = None):
        if log_file_path == None:
            log_file_path = '_' + self.abrv_commit_hash + '__commit_log.txt'
        
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:" %n---------%n H   commit hash:                                                                                                                 %H %n---------%n h   abbreviated commit hash:                                                                                                     %h %n---------%n T   tree hash:                                                                                                                   %T %n---------%n t   abbreviated tree hash:                                                                                                       %t %n---------%n P   parent hashes:                                                                                                               %P %n---------%n p   abbreviated parent hashes:                                                                                                   %p %n---------%n an   author name:                                                                                                                %an" > ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:" %n---------%n aN   author name (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                                     %aN %n---------%n ae   author email:                                                                                                               %ae %n---------%n aE   author email (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                                    %aE %n---------%n al   author email local-part (the part before the @ sign):                                                                       %al %n---------%n aL   author local-part (see %al) respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                      %aL %n---------%n ad   author date (format respects --date= option):                                                                               %ad %n---------%n aD   author date, RFC2822 style:                                                                                                 %aD" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:" %n---------%n ar   author date, relative:                                                                                                      %ar %n---------%n at   author date, UNIX timestamp:                                                                                                %at %n---------%n ai   author date, ISO 8601-like format:                                                                                          %ai %n---------%n aI   author date, strict ISO 8601 format:                                                                                        %aI %n---------%n as   author date, short format (YYYY-MM-DD):                                                                                     %as %n---------%n cn   committer name:                                                                                                             %cn %n---------%n cN   committer name (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                                  %cN" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:" %n---------%n ce   committer email:                                                                                                            %ce %n---------%n cE   committer email (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                                 %cE %n---------%n cl   author email local-part (the part before the @ sign):                                                                       %cl %n---------%n cL   author local-part (see %cl) respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                      %cL %n---------%n cd   committer date (format respects --date= option):                                                                            %cd %n---------%n cD   committer date, RFC2822 style:                                                                                              %cD %n---------%n cr   committer date, relative:                                                                                                   %cr" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:" %n---------%n ct   committer date, UNIX timestamp:                                                                                             %ct %n---------%n ci   committer date, ISO 8601-like format:                                                                                       %ci %n---------%n cI   committer date, strict ISO 8601 format:                                                                                     %cI %n---------%n cs   committer date, short format (YYYY-MM-DD):                                                                                  %cs %n---------%n d   ref names, like the --decorate option of git-log[1]:                                                                         %d %n---------%n D   ref names without the <comma that breaks my script> wrapping.:                                                               %D %n---------%n S   ref name given on the command line by which the commit was reached (like git log --source) only works with git log:          %S" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:" %n---------%n e   encoding:                                                                                                                    %e %n---------%n s   subject:                                                                                                                     %s %n---------%n f   sanitized subject line, suitable for a filename:                                                                             %f %n---------%n b   body:                                                                                                                        %b %n---------%n B   raw body (unwrapped subject and body):                                                                                       %B %n---------%n N   commit notes:                                                                                                                %N %n---------%n GG   raw verification message from GPG for a signed commit:                                                                      %GG" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:" %n---------%n G?   signature options - check doc for more info -- manually trimmed:                                                            %G? %n---------%n GS   show the name of the signer for a signed commit:                                                                            %GS %n---------%n GK   show the key used to sign a signed commit:                                                                                  %GK %n---------%n GF   show the fingerprint of the key used to sign a signed commit:                                                               %GF %n---------%n GP   show the fingerprint of the primary key whose subkey was used to sign a signed commit:                                      %GP %n---------%n gD   reflog selector - check doc for more info -- manually trimmed:                                                              %gD %n---------%n gd   shortened reflog selector; - check doc for more info -- manually trimmed:                                                   %gd" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:" %n---------%n gn   reflog identity name:                                                                                                       %gn %n---------%n gN   reflog identity name (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                            %gN %n---------%n ge   reflog identity email:                                                                                                      %ge %n---------%n gE   reflog identity email (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                           %gE %n---------%n gs   reflog subject:                                                                                                             %gs" >> ' + log_file_path)
        
    
    def json_log_tup(self):
        return (
                self.author         ,
                self.author_date    ,
                self.subject        ,
                self.body           ,
                self.changed_files_l,
                self.svn_rev_num    )
        
    def load_from_log_data(self, data_tup):
        self.author          = data_tup.pop(0)
        self.author_date     = data_tup.pop(0) 
        self.subject         = data_tup.pop(0) 
        self.body            = data_tup.pop(0) 
        self.changed_files_l = data_tup.pop(0)
        self.svn_rev_num     = data_tup.pop(0) 
        
    
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    '''                                                                           
            Misc. Testing Functions
    '''
    ''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
    def print_me(self, oneline = False):
        if oneline == True:
            print('Commit print_me:  '  , self.abrv_commit_hash, 'Svn_rev: ', self.svn_rev_num, '  Subject:  ', self.subject         )
        else:
            print('Commit print_me:  '  , self.abrv_commit_hash)
            print('  author         :  ', self.author          )
            print('  author_email   :  ', self.author_email    )
            print('  author_date    :  ', self.author_date     )
            print('  subject        :  ', self.subject         )
            print('  body           :  ', self.body            )
            print('  changed_files_l:  ', self.changed_files_l )
            print('  svn_rev_num    :  ', self.svn_rev_num     )
        

        
    
        

if __name__ == '__main__':
#     import repo_transfer
#     repo_transfer.main()

    from PIC_transfer import PIC_transfer
    PIC_transfer.main()

#     import Git_Repo
# #     Git_Repo.main()
#     g = Git_Repo.Git_Repo("C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\\ip_repo")
#     g.build_commit_l()
# #     g.commit_l[0]



































