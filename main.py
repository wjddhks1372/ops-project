from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis
import os  # 환경변수 제어를 위한 모듈 임포트

app = FastAPI()

# --- [Configuration] ---
# 환경변수에서 설정을 가져오며, 없을 경우 기본값(default)을 사용합니다.
# 보안상 민감한 정보(Password)는 기본값을 두지 않거나 빈 문자열로 처리합니다.

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None) # 비밀번호가 없으면 None

# Redis 연결 설정
# password 파라미터를 추가하여 환경변수로 받은 값을 실제로 사용하도록 수정했습니다.
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    루트 경로 접속 시 방문자 수를 카운트하고 HTML을 반환합니다.
    """
    try:
        # 방문자 수 증가
        count = r.incr('visitor_count')
    except redis.AuthenticationError:
        count = "Redis 인증 실패 (비밀번호 확인 필요)"
    except redis.ConnectionError:
        count = "Redis 연결 실패 (호스트/포트 확인 필요)"
    except Exception as e:
        count = f"오류 발생: {str(e)}"

    # HTML 응답 생성
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
            .count {{
                font-size: 5rem;
                font-weight: bold;
                color: #764ba2;
                margin: 0;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>현재 방문자 수</h1>
            <p class="count">{count}</p>
            <div class="footer">DevOps Portfolio Demo<br>Secured by Env Vars</div>
        </div>
    </body>
    </html>
    """
    return html_content