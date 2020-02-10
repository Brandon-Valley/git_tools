
try:
    # for eclipse code-completion 
    from submodules.git_tools import commit_log_format_strings as clfs
except:
    import commit_log_format_strings as clfs


VAR_DELIM = '@#$__VAR_DELIM__$#@'

class Git_Commit:
    # run_git_cmd will execute the given command inside the repo that initialized the Git_Commit class
    def __init__(self, abbreviated_commit_hash, run_git_cmd):
        self.run_git_cmd      = run_git_cmd
        self.abrv_commit_hash = abbreviated_commit_hash
        
        self.author          = None
        self.author_date     = None
        self.subject         = None
        self.body            = None
                           
        self.changed_files_l = []
        
        self.svn_rev_num     = None
        
#         self.log_commit_data('C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\bitbucket_repo_setup_scripts\\test__commit_log.txt')
        
#         self.run_git_cmd('git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n H   commit hash: ', print_output = True, print_cmd = True) 

        # build and run cmd to extract commit info
        cmd = 'git log ' + self.abrv_commit_hash + ' -n1 --oneline --pretty=format:"' + VAR_DELIM + clfs.AUTHOR_NAME \
                                                                                      + VAR_DELIM + clfs.AUTHOR_DATE \
                                                                                      + VAR_DELIM + clfs.SUBJECT     \
                                                                                      + VAR_DELIM + clfs.BODY        \
                                                                                + '"'
                                                                                       
        commit_data_str = self.run_git_cmd(cmd     , decode = True, print_output = True, print_cmd = True)
        commit_data_l = commit_data_str.split(VAR_DELIM)
        commit_data_l.pop(0) # remove first empty element

        self.author      = commit_data_l.pop(0)                                          
        self.author_date = commit_data_l.pop(0)                                          
        self.subject     = commit_data_l.pop(0)                                          
        self.body        = commit_data_l.pop(0)                
        
        
        # fill self.changed_files_l
        cmd = 'git show --name-only ' + self.abrv_commit_hash
        raw_commit_data_l = self.run_git_cmd(cmd     , decode = True, print_output = True, print_cmd = True)

        print(raw_commit_data_l)
        print(raw_commit_data_l[1])
        
        for line in reversed(raw_commit_data_l):
            print(line)
            if line[0] == '\n':
                break
            
            self.changed_files_l.append(line[:-1]) # trim newline
                        
        self.changed_files_l = list(reversed(self.changed_files_l)) # put back in abc order
                
                                                                                         
        # if this commit is from a git repo created by converting from an svn repo
        if 'git-svn-id: ' in self.body:
            self.svn_rev_num = self.body.split(' ')[-2].split('@')[1]
            
       
        
    # if no log_file_path is given, will log to default location
    def log_commit_data(self, log_file_path = None):
        if log_file_path == None:
            log_file_path = '_' + self.abrv_commit_hash + '__commit_log.txt'
        
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n H   commit hash:                                                                                                                 %H %n---------%n h   abbreviated commit hash:                                                                                                     %h %n---------%n T   tree hash:                                                                                                                   %T %n---------%n t   abbreviated tree hash:                                                                                                       %t %n---------%n P   parent hashes:                                                                                                               %P %n---------%n p   abbreviated parent hashes:                                                                                                   %p %n---------%n an   author name:                                                                                                                %an" > ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n aN   author name (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                                     %aN %n---------%n ae   author email:                                                                                                               %ae %n---------%n aE   author email (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                                    %aE %n---------%n al   author email local-part (the part before the @ sign):                                                                       %al %n---------%n aL   author local-part (see %al) respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                      %aL %n---------%n ad   author date (format respects --date= option):                                                                               %ad %n---------%n aD   author date, RFC2822 style:                                                                                                 %aD" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n ar   author date, relative:                                                                                                      %ar %n---------%n at   author date, UNIX timestamp:                                                                                                %at %n---------%n ai   author date, ISO 8601-like format:                                                                                          %ai %n---------%n aI   author date, strict ISO 8601 format:                                                                                        %aI %n---------%n as   author date, short format (YYYY-MM-DD):                                                                                     %as %n---------%n cn   committer name:                                                                                                             %cn %n---------%n cN   committer name (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                                  %cN" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n ce   committer email:                                                                                                            %ce %n---------%n cE   committer email (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                                 %cE %n---------%n cl   author email local-part (the part before the @ sign):                                                                       %cl %n---------%n cL   author local-part (see %cl) respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                      %cL %n---------%n cd   committer date (format respects --date= option):                                                                            %cd %n---------%n cD   committer date, RFC2822 style:                                                                                              %cD %n---------%n cr   committer date, relative:                                                                                                   %cr" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n ct   committer date, UNIX timestamp:                                                                                             %ct %n---------%n ci   committer date, ISO 8601-like format:                                                                                       %ci %n---------%n cI   committer date, strict ISO 8601 format:                                                                                     %cI %n---------%n cs   committer date, short format (YYYY-MM-DD):                                                                                  %cs %n---------%n d   ref names, like the --decorate option of git-log[1]:                                                                         %d %n---------%n D   ref names without the <comma that breaks my script> wrapping.:                                                               %D %n---------%n S   ref name given on the command line by which the commit was reached (like git log --source) only works with git log:          %S" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n e   encoding:                                                                                                                    %e %n---------%n s   subject:                                                                                                                     %s %n---------%n f   sanitized subject line, suitable for a filename:                                                                             %f %n---------%n b   body:                                                                                                                        %b %n---------%n B   raw body (unwrapped subject and body):                                                                                       %B %n---------%n N   commit notes:                                                                                                                %N %n---------%n GG   raw verification message from GPG for a signed commit:                                                                      %GG" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n G?   signature options - check doc for more info -- manually trimmed:                                                            %G? %n---------%n GS   show the name of the signer for a signed commit:                                                                            %GS %n---------%n GK   show the key used to sign a signed commit:                                                                                  %GK %n---------%n GF   show the fingerprint of the key used to sign a signed commit:                                                               %GF %n---------%n GP   show the fingerprint of the primary key whose subkey was used to sign a signed commit:                                      %GP %n---------%n gD   reflog selector - check doc for more info -- manually trimmed:                                                              %gD %n---------%n gd   shortened reflog selector; - check doc for more info -- manually trimmed:                                                   %gd" >> ' + log_file_path)
        self.run_git_cmd(print_cmd = True, shell = True, run_type = 'call', cmd = 'git log 34f2fab -n1 --oneline --pretty=format:" %n---------%n gn   reflog identity name:                                                                                                       %gn %n---------%n gN   reflog identity name (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                            %gN %n---------%n ge   reflog identity email:                                                                                                      %ge %n---------%n gE   reflog identity email (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                           %gE %n---------%n gs   reflog subject:                                                                                                             %gs" >> ' + log_file_path)

    # undo with git switch -
    def checkout(self):
        self.run_git_cmd('git checkout ' + self.abrv_commit_hash , print_output = True, print_cmd = True)
    
    
    
if __name__ == "__main__":
    import Git_Repo
#     Git_Repo.main()
    g = Git_Repo.Git_Repo("C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\svn_to_git_ip_repo\\ip_repo")
    g.build_commit_l()
#     g.commit_l[0]















