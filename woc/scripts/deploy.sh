#/bin/bash

## 第一次先执行下面命令安装一些包
# npm install hexo-deployer-git --save
# npm install hexo-generator-search --save
hexo clean
hexo generate
gulp  # 压缩HTML，必须在生成HTML之后压缩

#hexo server # 本地预览
hexo deploy  # 部署到Git上

# hexo new "文章题目"  # 创建新文章
# hexo new page "页面名称"  # 创建新页面






# # 快捷命令
# hexo g == hexo generate
# hexo d == hexo deploy
# hexo s == hexo server
# hexo n == hexo new


