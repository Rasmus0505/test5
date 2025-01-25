# 新建一个名为 create_vercel_project.py 的文件
# 将以下代码复制进去保存
# 在终端运行 python create_vercel_project.py

import os
from pathlib import Path

PROJECT_STRUCTURE = {
    "public": {
        "index.html": """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>智能学习系统</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>📚 间隔重复学习系统</h1>
        <div id="app">
            <div class="input-group">
                <input type="text" id="topic" placeholder="输入学习主题">
                <button onclick="startLearning()">开始学习</button>
            </div>
            <div id="card-container"></div>
        </div>
    </div>
    <script src="scripts.js"></script>
</body>
</html>""",
        
        "style.css": """body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background: #f0f2f5;
}

.container {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.input-group {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

input[type="text"] {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

button {
    padding: 10px 20px;
    background: #0070f3;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

#card-container {
    border-top: 1px solid #eee;
    padding-top: 20px;
}

.card {
    margin: 20px 0;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

.question {
    margin: 10px 0;
}

textarea {
    width: 100%;
    height: 80px;
    margin: 5px 0;
}""",
        
        "scripts.js": """let currentCardIndex = 0;

async function startLearning() {
    const topic = document.getElementById('topic').value;
    if (!topic) return alert('请输入学习主题！');

    try {
        const response = await fetch(`/api/generate?topic=${encodeURIComponent(topic)}`);
        const cards = await response.json();
        currentCardIndex = 0;
        renderCard(cards[currentCardIndex]);
    } catch (error) {
        alert('生成失败: ' + error.message);
    }
}

function renderCard(card) {
    const container = document.getElementById('card-container');
    container.innerHTML = `
        <div class="card">
            <h2>${card.title}</h2>
            <div class="knowledge">${card.knowledge}</div>
            <div class="questions">
                ${card.questions.map((q, i) => `
                    <div class="question">
                        <p>❓ 问题 ${i+1}: ${q.q}</p>
                        <textarea id="answer-${i}"></textarea>
                        <button onclick="showAnswer(${i})">显示答案</button>
                        <p class="answer" id="answer-${i}-ref" style="display:none">💡 参考答案: ${q.a}</p>
                    </div>
                `).join('')}
            </div>
            <button onclick="nextCard()">下一题</button>
        </div>
    `;
}

function showAnswer(index) {
    document.getElementById(`answer-${index}-ref`).style.display = 'block';
}

async function nextCard() {
    // 这里可以添加保存评分逻辑
    currentCardIndex++;
    const response = await fetch(`/api/generate?topic=${document.getElementById('topic').value}`);
    const cards = await response.json();
    if (currentCardIndex < cards.length) {
        renderCard(cards[currentCardIndex]);
    } else {
        document.getElementById('card-container').innerHTML = '<p>🎉 学习完成！</p>';
    }
}"""
    },
    
    "api": {
        "generate.py": """import os
import json
from openai import OpenAI
from http.server import BaseHTTPRequestHandler

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        topic = self.path.split('topic=')[1].split('&')[0]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content\": \"\"\"你是一个严格遵循JSON格式的课程生成器，请生成包含3个学习卡片的JSON数据，结构示例：
{
    "cards": [
        {
            "id": 1,
            "title": "示例标题",
            "knowledge": "知识点说明...",
            "questions": [
                {"q": "问题1", "a": "答案1"},
                {"q": "问题2", "a": "答案2"}
            ]
        }
    ]
}\"\"\"
                }, {
                    "role": "user",
                    "content": f"请为【{topic}】生成学习内容"
                }],
                temperature=0.3,
                response_format={"type": "json_object"},
                max_tokens=2000
            )
            
            data = json.loads(response.choices[0].message.content)
            self.wfile.write(json.dumps(data['cards']).encode())
            
        except Exception as e:
            self.wfile.write(json.dumps({"error": str(e)}).encode())"""
    },
    
    "requirements.txt": """openai>=1.0
python-dotenv>=1.0
python-http-server>=1.0
""",
    
    "vercel.json": """{
    "builds": [
        {
            "src": "api/*.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/api/(.*)",
            "dest": "api/$1"
        },
        {
            "src": "/(.*)",
            "dest": "/public/$1"
        }
    ]
}""",
    
    ".env": """# 请在此处添加你的OpenAI API密钥
OPENAI_API_KEY=你的API密钥
"""
}

def create_project():
    print("🚀 开始创建Vercel项目结构...")
    
    for path, contents in PROJECT_STRUCTURE.items():
        if isinstance(contents, dict):  # 处理目录
            dir_path = Path(path)
            dir_path.mkdir(exist_ok=True)
            print(f"📁 创建目录: {dir_path}")
            
            for file_name, file_content in contents.items():
                file_path = dir_path / file_name
                file_path.write_text(file_content, encoding="utf-8")
                print(f"📄 创建文件: {file_path}")
                
        else:  # 处理独立文件
            file_path = Path(path)
            file_path.write_text(contents, encoding="utf-8")
            print(f"📄 创建文件: {file_path}")
    
    print("\n✅ 项目创建完成！")
    print("请执行以下后续步骤：")
    print("1. 修改 .env 文件添加你的OpenAI API密钥")
    print("2. 运行命令安装依赖: pip install -r requirements.txt")
    print("3. 将项目上传到GitHub仓库")
    print("4. 到Vercel官网导入仓库部署")

if __name__ == "__main__":
    create_project()