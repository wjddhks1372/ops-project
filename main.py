from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis
import os

app = FastAPI()

# Redis 연결 설정
# docker-compose에서 서비스 이름을 'redis'로 설정할 것이므로 host에 'redis'를 입력합니다.
# 포트는 기본 6379입니다.
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    루트 경로 접속 시:
    1. Redis의 'visitor_count' 키 값을 1 증가시킵니다.
    2. 증가된 값을 가져와 HTML에 삽입하여 반환합니다.
    """
    try:
        # 방문자 수 증가 (incr 명령은 키가 없으면 0에서 시작하여 1을 더함)
        count = r.incr('visitor_count')
    except redis.ConnectionError:
        count = "Redis 연결 실패"

    # 예쁜 HTML 응답 생성 (CSS 포함)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>방문자 수 카운터</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                margin: 0;
                display: flex;
                justify_content: center;
                align_items: center;
                color: #333;
            }}
            .card {{
                background: white;
                padding: 2rem 4rem;
                border-radius: 20px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                text-align: center;
            }}
            h1 {{
                font-size: 1.5rem;
                color: #666;
                margin-bottom: 0.5rem;
            }}
            .count {{
                font-size: 5rem;
                font-weight: bold;
                color: #764ba2;
                margin: 0;
            }}
            .footer {{
                margin-top: 1.5rem;
                font-size: 0.8rem;
                color: #aaa;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>현재 방문자 수</h1>
            <p class="count">{count}</p>
            <div class="footer">DevOps Portfolio Demo<br>FastAPI + Redis</div>
        </div>
    </body>
    </html>
    """
    return html_content