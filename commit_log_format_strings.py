#                                                                                                                           
# ---------                                                                                                                 
#  H   commit hash:                                                                                                           34f2fab75c3c5341894b4d5b9d56a9095fea4474 
# ---------                                                                                                                 
#  h   abbreviated commit hash:                                                                                               34f2fab 
# ---------                                                                                                                 
#  T   tree hash:                                                                                                             c40f7aae7fc9b2ffba3a8ba5e9411a1b3746c1a5 
# ---------                                                                                                                 
#  t   abbreviated tree hash:                                                                                                 c40f7aa 
# ---------                                                                                                                 
#  P   parent hashes:                                                                                                         d47f9e9d6baa33f0a65e1f3753fd207795cf7589 
# ---------                                                                                                                 
#  p   abbreviated parent hashes:                                                                                             d47f9e9 
# ---------                                                                                                                 
#  an   author name:                                                                                                          Rosa(US), Matthew W 
AUTHOR_NAME = '%an'
# ---------                                                                                                                 
#  aN   author name (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                               Rosa(US), Matthew W 
# ---------                                                                                                                 
#  ae   author email:                                                                                                         matthew.w.rosa@boeing.com
AUTHOR_EMAIL = '%ae' 
# ---------                                                                                                                 
#  aE   author email (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                              matthew.w.rosa@boeing.com 
# ---------                                                                                                                 
#  al   author email local-part (the part before the @ sign):                                                                 %al 
# ---------                                                                                                                 
#  aL   author local-part (see %al) respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                %aL 
# ---------                                                                                                                 
#  ad   author date (format respects --date= option):                                                                         Thu Jul 11 18:46:48 2019 +0000 
AUTHOR_DATE = '%ad'
# ---------                                                                                                                 
#  aD   author date, RFC2822 style:                                                                                           Thu, 11 Jul 2019 18:46:48 +0000 
# ---------                                                                                                                 
#  ar   author date, relative:                                                                                                7 months ago 
# ---------                                                                                                                 
#  at   author date, UNIX timestamp:                                                                                          1562870808 
# ---------                                                                                                                 
#  ai   author date, ISO 8601-like format:                                                                                    2019-07-11 18:46:48 +0000 
# ---------                                                                                                                 
#  aI   author date, strict ISO 8601 format:                                                                                  2019-07-11T18:46:48+00:00 
# ---------                                                                                                                 
#  as   author date, short format (YYYY-MM-DD):                                                                               %as 
# ---------                                                                                                                 
#  cn   committer name:                                                                                                       Rosa(US), Matthew W 
# ---------                                                                                                                 
#  cN   committer name (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                            Rosa(US), Matthew W 
# ---------                                                                                                                 
#  ce   committer email:                                                                                                      matthew.w.rosa@boeing.com 
# ---------                                                                                                                 
#  cE   committer email (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                           matthew.w.rosa@boeing.com 
# ---------                                                                                                                 
#  cl   author email local-part (the part before the @ sign):                                                                 %cl 
# ---------                                                                                                                 
#  cL   author local-part (see %cl) respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                %cL 
# ---------                                                                                                                 
#  cd   committer date (format respects --date= option):                                                                      Thu Jul 11 18:46:48 2019 +0000 
# ---------                                                                                                                 
#  cD   committer date, RFC2822 style:                                                                                        Thu, 11 Jul 2019 18:46:48 +0000 
# ---------                                                                                                                 
#  cr   committer date, relative:                                                                                             7 months ago 
# ---------                                                                                                                 
#  ct   committer date, UNIX timestamp:                                                                                       1562870808 
# ---------                                                                                                                 
#  ci   committer date, ISO 8601-like format:                                                                                 2019-07-11 18:46:48 +0000 
# ---------                                                                                                                 
#  cI   committer date, strict ISO 8601 format:                                                                               2019-07-11T18:46:48+00:00 
# ---------                                                                                                                 
#  cs   committer date, short format (YYYY-MM-DD):                                                                            %cs 
# ---------                                                                                                                 
#  d   ref names, like the --decorate option of git-log[1]:                                                                    
# ---------                                                                                                                 
#  D   ref names without the <comma that breaks my script> wrapping.:                                                          
# ---------                                                                                                                 
#  S   ref name given on the command line by which the commit was reached (like git log --source) only works with git log:    34f2fab 
# ---------                                                                                                                 
#  e   encoding:                                                                                                                  
# ---------                                                                                                                
#  s   subject:                                                                                                               changed the adc to hold CS_ADC low during "Use adc" portion of statemachine.
SUBJECT = "%s" 
# ---------                                                                                                                
#  f   sanitized subject line, suitable for a filename:                                                                       changed-the-adc-to-hold-CS_ADC-low-during-Use-adc-portion-of-statemachine 
# ---------                                                                                                                
#  b   body:                                                                                                                  git-svn-id: https://wpns04.stl.mo.boeing.com/ANPsvn/Trunk/ip_repo@484 36f637cb-dc32-44b4-bb99-f64234f869f0
BODY = "%b"
#                                                                                                                          
# ---------                                                                                                                
#  B   raw body (unwrapped subject and body):                                                                                 changed the adc to hold CS_ADC low during "Use adc" portion of statemachine. 
#                                                                                                                          
# git-svn-id: https://wpns04.stl.mo.boeing.com/ANPsvn/Trunk/ip_repo@484 36f637cb-dc32-44b4-bb99-f64234f869f0               
#   
# ---------                                                                                                                
#  N   commit notes:                                                                                                              
# ---------                                                                                                                
#  GG   raw verification message from GPG for a signed commit:                                                                    
# ---------                                                                                                                
#  G?   signature options - check doc for more info -- manually trimmed:                                                      N 
# ---------                                                                                                                
#  GS   show the name of the signer for a signed commit:                                                                           
# ---------                                                                                                                
#  GK   show the key used to sign a signed commit:                                                                                 
# ---------                                                                                                                
#  GF   show the fingerprint of the key used to sign a signed commit:                                                              
# ---------                                                                                                                
#  GP   show the fingerprint of the primary key whose subkey was used to sign a signed commit:                                     
# ---------                                                                                                                
#  gD   reflog selector - check doc for more info -- manually trimmed:                                                             
# ---------                                                                                                                
#  gd   shortened reflog selector; - check doc for more info -- manually trimmed:                                                  
# ---------                                                                                                                
#  gn   reflog identity name:                                                                                                      
# ---------                                                                                                                
#  gN   reflog identity name (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                           
# ---------                                                                                                                
#  ge   reflog identity email:                                                                                                     
# ---------                                                                                                                
#  gE   reflog identity email (respecting .mailmap, see git-shortlog[1] or git-blame[1]):                                          
# ---------                                                                                                                
#  gs   reflog subject:                                                                                                            