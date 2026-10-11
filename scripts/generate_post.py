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

# 日记的“素材池”
fragments = [
    "今天去了图书馆。",
    "今天没出门。",
    "今天下雨了。",
    "今天学了下电脑的使用呢。",
    "今天看了会儿书。",
    "今天收到一条消息。",
    "今天有一场live呢。",
    "今天翻到以前的照片。",
    "今天什么也没做。",
    "今天鱼缸里的鱼死了。",
    "今天日记里有一页不是我写的。",
    "今天有人敲门，开门没人。",
    "今天在镜子里看到自己，愣了一下。",
    "今天鞋是湿的，但我没出门。",
    "今天去了事务所。",
    "今天拍了一场戏。",
    "今天看了剧本。",
    "今天回家很晚。",
    "今天收到一封粉丝的信。"
]

is_off = random.randint (0,1);
if is_off:
    abnormal = "在文章中穿插一些“不对劲”的细节，但不解释，不渲染，点到为止，少量即可。（风格参考旧核、怪核等）"
else:
    abnormal = "这是一篇完全正常的日记，不用加入任何异常细节"

# 3. 构建提示词
prompt = f"""请以日本流行音乐偶像团体"CHAM!"成员中的偶像歌手未麻（人物源自电影《未麻的部屋》）的身份，以第一人称，写一篇日记。


要求：
- 使用 Markdown 格式。
- 3 到 10 段，每段1-5句话。
- 语气平静、简短、不展开，捎带一点可爱，稍微有一点意识流。
- {abnormal}
- 不要用“我感到恐惧”“我很害怕”一类的词。不安感来自于事实本身。
- 标题语法正确，语句通顺，但又一丝丝怪异感。

参考风格：
今天去了事务所。经纪人说我最近状态不错。
回家路上买了鱼食。鱼缸里的鱼只剩一条了。
我记得昨天还有三条。
可能是记错了。
晚上写了日记。今天就这样。

你可以从下面的片段里选几个作为素材：
{random.sample(fragments, 3)}
"""

# 4. 调用 DeepSeek API 生成文章
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个写日记的人。你只记录事实，只记录感受，不解释。"},
        {"role": "user", "content": prompt}
    ],
    temperature=0.8,
    max_tokens=2000
)

content = response.choices[0].message.content

# 5. 保存为 Markdown 文件
import re

date_str = datetime.now().strftime('%Y-%m-%d')
filename = f"content/posts/{date_str}.md"

os.makedirs(os.path.dirname(filename), exist_ok=True)

front_matter = f"""---
title: "{date_str}"
date: {datetime.now().isoformat()}
draft: false
author: '雾越未麻'
categories: ["日记"]
hideMeta: true
ShowReadingTime: false
ShowShareButtons: false
ShowPostNavLinks: false
comments: false
---

"""

with open(filename, "w", encoding="utf-8") as f:
    f.write(front_matter + content)

print(f"日记已生成：{filename}")