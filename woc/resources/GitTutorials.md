Push
--------
- 建立远程分支：git push --set-upstream origin <branchName> --force 
- 删除远处仓库分支（远程master不能删除）：git push origin -d <branchName> 
- 删除远处仓库tag：git push origin -d tag <branchName> 

Branch
---------

- 查看本地所有分支：git branch 
  查看远程所有分支：git branch -r 
- 查看本地和远程所有分支：git branch -a  
- 查看本地和远程所有分支的最后一次操作：git branch -av 
-  删除本地分支：git branch -d <branchName>
- 强行删除分支：git branch -D <branchName> 
- 分支改名：git branch -m <branchName> <NewBranchName> 
- 强制分支改名：git branch -M <branchName> <NewBranchName> 


    
Checkout
------------

- 创建并切换到新分支：git checkout -b <branchName> 
- 快速切换到上一次的分支：git checkout - 
- 在本地master切换到远程已有的远程分支：git checkout --track origin/<branchName>  



Merge
-----------

- 合并分支到当前分支上：git merge <branchName> 


# 暂存操作
- git stash 暂存当前修改
- git stash apply 恢复最近的一次暂存
- git stash pop 恢复暂存并删除暂存记录
- git stash list 查看暂存列表
- git stash drop 暂存名(例：stash@{0}) 移除某次暂存
- git stash clear 清除暂存
# 回退操作
- git log --oneline查看提交日志
- git relog  显示所有的提交日志，包括已经删除的，当你回退后后悔了非常有用
- git reset --hard HEAD^ 回退到上一个版本
- git reset --hard ahdhs1(commit_id) 回退到某个版本
- git checkout -- file撤销修改的文件(如果文件加入到了暂存区，则回退到暂存区的，如果文件加入到了版本库，则还原至加入版本库之后的状态)
- git reset HEAD file 撤回暂存区的文件修改到工作区
# 标签操作
- git tag 标签名 添加标签(默认对当前版本)
- git tag 标签名 commit_id 对某一提交记录打标签
- git tag -a 标签名 -m ‘描述’ 创建新标签并增加备注
- git tag 列出所有标签列表
- git show 标签名 查看标签信息
- git tag -d 标签名 删除本地标签
- git push origin 标签名 推送标签到远程仓库
- git push origin –tags 推送所有标签到远程仓库
- git push origin :refs/tags/标签名 从远程仓库中删除标签
# 常规操作
- git push origin test 推送本地分支到远程仓库
- git rm -r –cached 文件/文件夹名字 取消文件被版本控制
- git reflog 获取执行过的命令
- git log –graph 查看分支合并图
- git merge –no-ff -m ‘合并描述’ 分支名 不使用Fast forward方式合并，采用这种方式合并可以看到合并记录
- git check-ignore -v 文件名 查看忽略规则
- git add -f 文件名 强制将文件提交
# git创建项目仓库
- git init 初始化
- git remote add origin url 关联远程仓库
- git pull
- git fetch 获取远程仓库中所有的分支到本地
# 忽略已加入到版本库中的文件
- git update-index –assume-unchanged file 忽略单个文件
- git rm -r –cached 文件/文件夹名字 (. 忽略全部文件)
# 取消忽略文件
- git update-index –no-assume-unchanged file
# 拉取、上传免密码
- git config –global credential.helper store

# 使用gitignore删除已经提交的文件
```shell
git rm -r --cache .
git add .
git commit -m ".gitignore now work"
git push
```

# 设置git提交时最大文件大小
git config --global http.postBuffer 524288000



### Getting & Creating Projects

| Command | Description |
| ------- | ----------- |
| `git init` | Initialize a local Git repository |
| `git clone ssh://git@github.com/[username]/[repository-name].git` | Create a local copy of a remote repository |

### Basic Snapshotting

| Command | Description |
| ------- | ----------- |
| `git status` | Check status |
| `git add [file-name.txt]` | Add a file to the staging area |
| `git add -A` | Add all new and changed files to the staging area |
| `git commit -m "[commit message]"` | Commit changes |
| `git rm -r [file-name.txt]` | Remove a file (or folder) |

### Branching & Merging

| Command | Description |
| ------- | ----------- |
| `git branch` | List branches (the asterisk denotes the current branch) |
| `git branch -a` | List all branches (local and remote) |
| `git branch [branch name]` | Create a new branch |
| `git branch -d [branch name]` | Delete a branch |
| `git push origin --delete [branch name]` | Delete a remote branch |
| `git checkout -b [branch name]` | Create a new branch and switch to it |
| `git checkout -b [branch name] origin/[branch name]` | Clone a remote branch and switch to it |
| `git branch -m [old branch name] [new branch name]` | Rename a local branch |
| `git checkout [branch name]` | Switch to a branch |
| `git checkout -` | Switch to the branch last checked out |
| `git checkout -- [file-name.txt]` | Discard changes to a file |
| `git merge [branch name]` | Merge a branch into the active branch |
| `git merge [source branch] [target branch]` | Merge a branch into a target branch |
| `git stash` | Stash changes in a dirty working directory |
| `git stash clear` | Remove all stashed entries |

### Sharing & Updating Projects

| Command | Description |
| ------- | ----------- |
| `git push origin [branch name]` | Push a branch to your remote repository |
| `git push -u origin [branch name]` | Push changes to remote repository (and remember the branch) |
| `git push` | Push changes to remote repository (remembered branch) |
| `git push origin --delete [branch name]` | Delete a remote branch |
| `git pull` | Update local repository to the newest commit |
| `git pull origin [branch name]` | Pull changes from remote repository |
| `git remote add origin ssh://git@github.com/[username]/[repository-name].git` | Add a remote repository |
| `git remote set-url origin ssh://git@github.com/[username]/[repository-name].git` | Set a repository's origin branch to SSH |

### Inspection & Comparison

| Command | Description |
| ------- | ----------- |
| `git log` | View changes |
| `git log --summary` | View changes (detailed) |
| `git log --oneline` | View changes (briefly) |
| `git diff [source branch] [target branch]` | Preview changes before merging |
