---
name: commit
description:
  "Commit coursework in this study repo the house way: only the current chat's
  changes, one commit per logical change, `<course-folder>: description`, one
  course per commit, notebooks committed only with fresh outputs. Use whenever
  the user runs /commit, says 'commit this', 'закоммить', 'сделай коммит',
  'зафиксируй изменения', or otherwise asks for work here to be committed —
  including when they say nothing about message format, since getting the scope
  and the per-course split right is the whole point of this skill."
user-invocable: true
argument-hint: [optional hint about what the change was for]
model: sonnet
effort: medium
allowed-tools:
  Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*),
  Bash(git log:*), Bash(jq:*)
---

- commit like `<course-folder>: description`, e.g.
  `21-ai-big-data: pr-1 data loading and filtering`; changes outside course
  folders use `repo: description`
- one course per commit; split only independent logical changes, keep one
  finished task or practice part in one commit
- stage only files this chat changed, by explicit path; leave other changes and
  unpushed commits alone
- `.ipynb`: commit only if every non-empty code cell has an execution count and
  no error output; otherwise stop and tell the user to run all cells and save
  first. This must print `0`:
  `jq '[.cells[] | select(.cell_type=="code" and ((.source|if type=="array" then join("") else . end)|test("\\S"))) | select(.execution_count==null or any(.outputs[]; .output_type=="error"))] | length' file.ipynb`
- never stage virtual environments, caches or data files the practices write;
  if such files show up untracked, ask instead of adding them
- do not push unless asked: the repo is public
