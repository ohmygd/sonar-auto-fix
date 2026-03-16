# sonar-autofix
sonar自动修复

📖 简介
sonar-auto-fix 是一个 Qoder 编辑器技能，能够自动检查代码的 SonarQube 问题并自动修复。它通过接收外部参数，执行 SonarQube 扫描，获取问题列表，然后结合 AI 能力自动生成修复方案。

✨ 功能特点
✅ 一键执行：输入 sonar-autofix 命令即可触发完整流程

✅ 参数化配置：支持自定义 SonarQube 地址、Token、项目信息等

✅ 自动扫描：自动执行 Maven SonarQube 插件进行代码扫描

✅ AI 修复：根据问题列表自动生成修复方案并应用到代码

🚀 快速开始
1. 安装技能
将本技能文件夹放入 Qoder 技能目录：
用户级（所有项目可用）：~/.qoder/skills/sonar-autofix/
项目级（当前项目可用）：你的项目根目录/.qoder/skills/sonar-autofix/
2. 在 Qoder 中使用
打开 Qoder 聊天面板（快捷键：Ctrl + L）
切换到 Agent 模式（在输入框下拉菜单中选择）
输入命令：
sonar-autofix -sonarUrl=http://你的sonar地址:9000/sonar -token=你的token -author=你的名字 -settingPath=F:\你的路径\settings.xml -projectKey=你的项目Key
📝 参数详解
参数名	必填	默认值	示例	说明
sonarUrl	✅	-	default	SonarQube 服务器地址
token	✅	-	default	SonarQube 认证 Token
author	✅	-	default	代码作者，用于修复记录
settingPath	✅	-	default	Maven settings.xml 路径
projectKey	✅	-	default	项目包信息，格式：公司名:包名