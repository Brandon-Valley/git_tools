from subprocess import PIPE, CalledProcessError, check_call, Popen
from util_submodules__gu.subprocess_utils import subprocess_utils as su
import os

os.chdir('C:\\Users\\mt204e\\Documents\\projects\\Bitbucket_repo_setup\\repos\\ip_repo')

cmd = "git checkout d117685 -f "
print('start')
with open("log.txt", "w") as f:
    try:
        check_call("git checkout d117685 -f ", stderr=f)
        df = Popen("git checkout d117685 -f ", stdout=PIPE)
#         check_call("echo hi ", stderr=f)
#         df = Popen("echo hi ", stdout=PIPE)
        output, err = df.communicate()
    except CalledProcessError as e:
        print(e)
#         exit(1)

print('end')


# s = []
# try:
#     check_call("git checkout d117685 -f ", stderr=s)
#     df = Popen("git checkout d117685 -f ", stdout=PIPE)
#     output, err = df.communicate()
# except CalledProcessError as e:
#     print(e)
#     exit(1)
# 
# print('s:  ', s)








# out  = su.run_cmd_popen(cmd, print_output = False, print_cmd = True, shell = False, decode = False, strip = False, always_output_list = False)
# 
# print(out)