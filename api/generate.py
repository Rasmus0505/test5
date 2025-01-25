import os
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
                    "content": """你是一个严格遵循JSON格式的课程生成器，请生成包含3个学习卡片的JSON数据，结构示例：
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
}"""
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
            self.wfile.write(json.dumps({"error": str(e)}).encode())