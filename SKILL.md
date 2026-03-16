---
name: sonar自动修复
description: 自动检查代码的sonar问题, 然后进行问题修复，支持自定义参数和代码作者信息, 命令名称: sonar-autofix
---

## 功能描述
执行流程严格参考注意事项, 当执行 `sonar-autofix` 命令时，可接收外部参数，执行步骤如下：
1. 根据传入的参数执行 SonarQube 代码扫描
2. 执行 `sonar_problem_search.py` 脚本获取扫描结果
3. 根据获取到的问题列表，结合代码作者信息进行自动修复

## 参数说明
### 支持的外部参数
| 参数名 | 类型 | 是否必填 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| `sonarUrl` | string | 是 | `http://default/sonar` | SonarQube 服务器地址 |
| `token` | string | 是 | `default` | SonarQube 认证 Token |
| `settingPath` | string | 是 | `default` | Maven settings.xml 路径 |
| `author` | string | 是 | `default` | 代码作者（用于修复记录和提交信息）|
| `projectKey` | string | 是 | `default` | 项目包信息, 公司名:包名|

## 触发方式
### 命令格式
sonar-autofix [-参数名=参数值] [-参数名=参数值] ...
### 使用示例
**示例：完整参数示例**
sonar-autofix -sonarUrl=http://127.0.0.1:9000/sonar -token=fe38bf62a0xc7c18bb56ddvcca2e1d222dacd3ab -author=mac -settingPath=F:\myPath\settings.xml --projectKey=com.tt.mm:mcProject

## 命令对应执行流程
### 步骤1：进行sonar检查
进行sonar检查, 执行如下命令:
```bash
mvn org.sonarsource.scanner.maven:sonar-maven-plugin:3.11.0.3922:sonar "-Dsonar.host.url={{sonarUrl}}" "-Dsonar.login={{token}}"  -f ./pom.xml -s {{settingPath}}
```
### 步骤2：获取 SonarQube 问题
执行python脚本, 获取上一步骤对应的sonar检查结果
```bash
python ./scripts/sonar_problem_search.py --sonarQubeUrl={{sonarUrl}} --sonarToken={{token}} --projectKey={{projectKey}}
```
### 步骤3：根据输出的sonar内容, 自动修复sonar问题
根据上一步骤获取到的结果, 自动解决sonar问题, 结合代码作者信息