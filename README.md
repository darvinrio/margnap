# margnap - A Pangram beater

Pangram Labs have an AI detector, that detects AI text. 
Can I build a RL tuned model to beat the AI detector?

## helpful commands

### python

```sh
# check ruff issues
ruff check
# fix ruff issues
ruff check --fix  
# format ruff
ruff format 
# check types
ty check
# run all checks
pre-commit run --all-files
```

```sh
# add repo to python path
export PYTHONPATH="$PWD:$PYTHONPATH"
```

### gitHub

```bash
# Delete local merged branches
git branch --merged | grep -v '\*' | xargs -n 1 git branch -d

# Prune origin deleted branches
git remote prune origin
```
