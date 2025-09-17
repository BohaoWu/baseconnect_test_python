# articles/services.py
from django.utils import timezone
import os, re
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

from .models import Articles

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_news(url: str):
    resp = requests.get(url, timeout=10)
    resp.encoding = resp.apparent_encoding
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    
    title_tag = soup.find("title")
    title = title_tag.get_text().strip() if title_tag else ""
    title = title.split("|")[0].strip()
        
    paras = [p.get_text(strip=True) for p in soup.select("div.body-text p")]
    text = "\n\n".join(paras)

    date = soup.find("time").get("datetime")
    
    article = Articles(
        url=url,
        title=title,
        text=text,
        abstract="",
        risk_score=0,
        created_at=timezone.now(),
        pub_date=date
    )
    
    return article

def get_abstract(text: str) -> str:
    response = get_client().chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "あなたは要約を作るアシスタントです。"},
            {"role": "user", "content": f"100文字の要約を作成する:\n\n{text}"}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def score_risk(text: str) -> int:
    prompt = (
        "次のニュースの社会的リスクを0-100で数値のみで返答してください。"
        "評価基準：被害範囲・被害程度・社会的影響・死傷者/被害額。"
        "殺人事件は50点基準。数値のみ出力：\n\n" + text[:6000]
    )
    resp = get_client().chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "数値判定アシスタント"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    raw = (resp.choices[0].message.content or "").strip()
    m = re.search(r"\d{1,3}", raw)
    score = int(m.group())
    return score