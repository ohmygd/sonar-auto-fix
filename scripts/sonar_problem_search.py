import argparse
import requests
from requests.auth import HTTPBasicAuth

def parse_args():
    """解析命令行参数，包括 --sonar-url"""
    parser = argparse.ArgumentParser(description='sonar自动修复入参获取')
    
    # 核心参数：sonar-url
    parser.add_argument('--sonarQubeUrl', '-u', 
                       default='',
                       help='SonarQube 服务器地址')
    # 其他参数
    parser.add_argument('--sonarToken', '-t', 
                       default='',
                       help='SonarQube 认证 Token')
    parser.add_argument('--projectKey', '-p', default='',
                       help='项目key, 公司名:包名')
    return parser.parse_args()

# ===== 配置区域 =====
args = parse_args()
SONAR_QUBE_URL = args.sonarQubeUrl # 你的SonarQube基础URL
SONAR_TOKEN = args.sonarToken # 替换成你生成的Token
PROJECT_KEY = args.projectKey # 你的项目Key
# ===================

# API端点
api_endpoint = f"{SONAR_QUBE_URL}/api/issues/search"

# 请求参数
params = {
    "componentKeys": PROJECT_KEY,  # 指定项目
    "resolved": "false",           # 只查询未解决的问题
    "types": "CODE_SMELL",         # 问题类型为代码坏味道
    "ps": 500,                     # 每页结果数 (page size)，最大500，可根据需要调整
    # "p": 1                        # 页码，如果结果超过100，需要分页获取
}

# 认证信息：使用Token，注意Token后面要跟一个空字符串作为密码
# 或者可以使用 auth=HTTPBasicAuth(SONAR_TOKEN, '') 这种更标准的方式 [citation:2]
auth = HTTPBasicAuth(SONAR_TOKEN, '')

# 请求头，有时可能需要，但通常不是必须的
headers = {
    "Content-Type": "application/x-www-form-urlencoded" # API文档推荐 [citation:2]
}

try:
    print(f"正在从 SonarQube 获取项目 '{PROJECT_KEY}' 的代码坏味道...")
    response = requests.get(api_endpoint, params=params, auth=auth, headers=headers, timeout=30)
    response.raise_for_status()  # 检查HTTP错误（如4xx, 5xx）

    data = response.json()
    issues = data.get('issues', [])
    total = data.get('total', 0)

    print(f"共找到 {total} 个未解决的代码坏味道问题。\n")

    if not issues:
        print("没有获取到具体问题列表，请检查参数或确认项目是否有对应问题。")
    else:
        # 遍历并打印每个问题的信息
        for idx, issue in enumerate(issues, 1):
            print(f"--- 问题 {idx} ---")
            print(f"  消息: {issue.get('message')}")
            print(f"   severity: {issue.get('severity')}") # 严重程度 (INFO, MINOR, MAJOR, CRITICAL, BLOCKER)
            print(f"  文件路径: {issue.get('component')}")
            print(f"  行号: {issue.get('line')}")
            print(f"  规则Key: {issue.get('rule')}")
            print(f"  技术债务(分钟): {issue.get('effort')}") # 修复预估时间 [citation:6][citation:10]
            print(f"  状态: {issue.get('status')}")
            print(f"  创建时间: {issue.get('creationDate')}")
            print("-" * 20)

        # 如果总数超过单页数量，可以在这里添加循环处理分页
        if total > params['ps']:
            print(f"提示：共有 {total} 个问题，当前只显示了前 {params['ps']} 个。")
            print("你可以通过循环 'p' 参数来获取所有页面的数据。")

except requests.exceptions.Timeout:
    print("错误：请求超时，请检查网络连接或稍后重试。")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e}")
    if response.status_code == 401:
        print("认证失败，请检查你的 Token 是否正确。")
    elif response.status_code == 403:
        print("权限不足，请确保 Token 关联的用户有浏览该项目的权限。 [citation:2]")
    else:
        print(f"响应内容: {response.text}")
except Exception as e:
    print(f"发生未知错误: {e}")
