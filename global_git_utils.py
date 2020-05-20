if __name__ == "__main__": 
    from   usms.subprocess_utils  import subprocess_utils  as su
else:
    from . usms.subprocess_utils  import subprocess_utils  as su



def get_user_name(print_output = False, print_cmd = False):
    cmd = 'git config user.name'
    return su.run_cmd_popen(cmd, print_output, print_cmd, decode = True)


def get_user_email(print_output = False, print_cmd = False):
    cmd = 'git config user.email'
    return su.run_cmd_popen(cmd, print_output, print_cmd, decode = True)


def set_user_name(new_user_name, print_output = False, print_cmd = False):
    cmd = 'git config user.name="' + new_user_name + '"'
    su.run_cmd_popen(cmd, print_output, print_cmd)
    

def set_user_email(new_user_email, print_output = False, print_cmd = False):
    cmd = 'git config user.email="' + new_user_email + '"'
    su.run_cmd_popen(cmd, print_output, print_cmd)
    
    
    
    
    
    
if __name__ == '__main__':
    print('In Main:  global_git_utils')
    import repo_transfer
    repo_transfer.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    print('End Of Main:  global_git_utils')