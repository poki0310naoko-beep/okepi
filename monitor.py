import requests
from bs4 import BeautifulSoup
import os

# 設定
TARGET_URL = "https://okepi.net/bbs/posting?Searching=false&Keyword=%E3%82%B4%E3%83%BC%E3%82%B9%E3%83%88%26%E3%83%AC%E3%83%87%E3%82%A3&ExConditionalPost=true&TradeType=1&SortKey=UpdateTimeDesc"
HEADERS = {"User-Agent": "Mozilla/5.0"}
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

def check_okepi():
    last_id = ""
    # 前回URLの読み込み（ファイルがなくても無視する）
    if os.path.exists("last_id.txt"):
        try:
            with open("last_id.txt", "r") as f:
                last_id = f.read().strip()
        except:
            pass

    # サイト取得
    try:
        r = requests.get(TARGET_URL, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        link_tag = soup.select_one('a[href^="/bbs/posting/"]')
        
        if not link_tag:
            print("No posts found.")
            return

        current_url = "https://okepi.net" + link_tag.get('href')

        # 更新があれば通知
        if current_url != last_id:
            if DISCORD_WEBHOOK_URL:
                requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🔔 新着！\n{current_url}"})
                print(f"Sent notification: {current_url}")
            
            # 保存を試みる（ここでエラーが出ても無視するように修正）
            try:
                with open("last_id.txt", "w") as f:
                    f.write(current_url)
                print("Successfully saved last_id.txt")
            except Exception as e:
                print(f"Save failed but ignoring: {e}")
        else:
            print("No update.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_okepi()
