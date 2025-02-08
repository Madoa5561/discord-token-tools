import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from colorama import init, Fore


init(autoreset=True)

def read_tokens_from_file(file_path: str) -> list:
    """ファイルからトークンを読み込む関数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = file.read().splitlines()
        print(Fore.GREEN + "[+] トークンの読み込みに成功しました。")
        return tokens
    except FileNotFoundError:
        print(Fore.RED + f"エラー: {file_path} が見つかりません。")
        return []

def join_check(token: str, myid:str, guild_id: str) -> bool:
    """サーバーへの参加を確認する関数"""
    url = f"https://discord.com/api/v9/users/{myid}/profile"
    headers = {
        "Authorization": token,
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImphLUpQIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMxLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tLz9kaXNjb3JkdG9rZW49TVRJNE56ZzFOalk1TURFM05URTFNakUwTUEuR2U4NzlLLllFdzFwQ3hMMjNtRDdGM2FNMXpKZVp0dDFaTjRJY1pDMDNGX3BjIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6Imh0dHBzOi8vZGlzY29yZC5jb20vP2Rpc2NvcmR0b2tlbj1NVEk0TnpnMU5qWTVNREUzTlRFMU1qRTBNQS5HZTg3OUsuWUV3MXBDeEwyM21EN0YzYU0xekplWnR0MVpONEljWkMwM0ZfcGMiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiJkaXNjb3JkLmNvbSIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjM1MTI0NywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }
    data = {
        "guilds": {
            guild_id: {
                "muted": False
            }
        }
    }
    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        print(Fore.GREEN + f"[+] {token} でサーバーに参加成功")
        return True
    return False

def first_check(token: str, invite_code: str) -> str:
    """招待コードからギルドIDを取得する関数"""
    url = f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true&with_expiration=true"
    headers = {
        "Authorization": token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("guild_id")
    return None

def open_session(token: str):
    """Discordセッションを開く関数"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    script = """
          function login(token) {
          setInterval(() => {
          document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
          }, 50);
          setTimeout(() => {
          location.reload();
          }, 2500);
          }
          """
    driver.get("https://discord.com/login")
    driver.execute_script(script + f'\nlogin("{token}")')
    input(Fore.YELLOW + "[~] 参加が完了したらENTERキーを押してください...")
    print(Fore.GREEN + f"[+] トークン {token} で参加が完了しました。")
    driver.quit()

def extract_invite_code(invite_url: str) -> str:
    """Discordの招待URLから招待コードを抽出する関数"""
    if "discord.gg/" in invite_url:
        return invite_url.split("discord.gg/")[1]
    elif "discord.com/invite/" in invite_url:
        return invite_url.split("discord.com/invite/")[1]
    return invite_url

def main():
    """メイン関数"""
    global guild_id
    tokens = read_tokens_from_file("token.txt")
    if not tokens:
        print(Fore.RED + "トークンが見つかりません。終了します。")
        return
    print(Fore.GREEN + f"[+] サーバーへの参加を開始します\nトークンの総数: {len(tokens)}")
    for token in tokens:
        open_session(token)
    print(Fore.GREEN + "[+] 完了しました")

if __name__ == "__main__":
    main()
