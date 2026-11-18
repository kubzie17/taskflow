Record the two commit IDs related to the diagnostic file:

f7328f2 (HEAD -> master) Remove diagnostic file from current tree
b9ab68f Add temporary diagnostic settings


git show HEAD~1:app/dispatch.local.env:
DISPATCH_DIAGNOSTIC=TRAINING_ONLY_NOT_A_CREDENTIAL

git check-ignore -v --no-index app/dispatch.local.env
echo $?
exit code = 1

git check-ignore -q --no-index .env.example
echo $?
exit code = 1

git ls-files -- .env.example
.env.example


Expected after a correct Git ignore repair: exit code 0:

hannah.blake@LT-16120 taskflow % git check-ignore -q --no-index app/dispatch.local.env
hannah.blake@LT-16120 taskflow % echo $?                                              
0

Expected: exit code 1, meaning the example is not ignored:
hannah.blake@LT-16120 taskflow % git check-ignore -q --no-index .env.example
hannah.blake@LT-16120 taskflow % echo $?                                    
1


Who should be informed: the cyber team, owner of the credential, whoever administers the system it authenticates to, repo maintainers, consumers who need to switch to the new credential before the old one dies
How the exposed credential should be revoked or rotated: Rotate at the source: issue the new credential, distribute and deploy it, then revoke the old one, then verify.
Which additional locations would need investigation: This repo's object store, any clone/fork, ci run logs and artifacts, docker images if not excluded from file, backups etc
How to verify the old credential no longer works: attempt to authenticate with the old value and confirm you're rejected with a 401
