import os
import json
import random
from datetime import datetime
from openai import OpenAI

# 1. 初始化 DeepSeek 客户端（兼容 OpenAI 格式）
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

# 2. 读取选题池
with open("topics.json", "r", encoding="utf-8") as f:
    topics = json.load(f)

# 随机选一个选题
topic = random.choice(topics)

# 3. 构建提示词
prompt = f"""请以专业的技术博客作者身份，写一篇关于“{topic['title']}”的文章。
文章简介：{topic['description']}

要求：
- 使用 Markdown 格式。
- 包含 YAML Front Matter，字段包括：title, date, draft (设为 false), tags, description。
- date 使用当前日期 {datetime.now().strftime('%Y-%m-%d')}。
- 文章结构清晰，包含引言、正文（分小节）、代码示例、总结。
- 字数在 800-1500 字之间。
- 语言风格：专业、友好、适合个人博客读者。
"""

# 4. 调用 DeepSeek API 生成文章
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一位专业的技术博客作者。"},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=4000
)

content = response.choices[0].message.content

# 5. 保存为 Markdown 文件
import re

# 用日期 + 序号作为文件名，避免中文和空格
date_str = datetime.now().strftime('%Y-%m-%d')
filename = f"content/posts/{date_str}-ai-post.md"

# 如果当天已有一篇，加序号
counter = 1
while os.path.exists(filename):
    counter += 1
    filename = f"content/posts/{date_str}-ai-post-{counter}.md"
safe_title = "".join(c for c in topic['title'] if c.isalnum() or c in " -_").rstrip()
filename = f"content/posts/{datetime.now().strftime('%Y-%m-%d')}-{safe_title}.md"

os.makedirs(os.path.dirname(filename), exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

print(f"文章已生成：{filename}")