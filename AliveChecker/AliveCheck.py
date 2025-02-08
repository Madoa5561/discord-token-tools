import asyncio
import aiohttp
from colorama import init, Fore

init(autoreset=True)

def read_tokens_from_file(file_path: str) -> list:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = file.read().splitlines()
        print(Fore.GREEN + "[+] トークンの読み込みに成功しました。")
        return tokens
    except FileNotFoundError:
        print(Fore.RED + f"エラー: {file_path} が見つかりません。")
        return []

async def check_token_status(token: str, session: aiohttp.ClientSession) -> str:
    url = "https://discord.com/api/v9/users/@me/settings"
    headers = {
        "authorization": token,
        "content-type": "application/json"
    }
    data = {
        "status": "online"
    }
    try:
        async with session.patch(url, headers=headers, json=data) as response:
            if response.status == 200:
                print(Fore.GREEN + f"[+] {token} Alive")
                return "生存"
            elif response.status == 401:
                print(Fore.RED + f"[-] {token} Dead")
                return "認証エラー"
            elif response.status == 403:
                print(Fore.RED + f"[-] {token} Dead")
                return "アカウントの確認エラー"
            else:
                print(Fore.RED + f"[-] {token} Dead")
                return "不明な通信エラー"
    except Exception as e:
        print(Fore.RED + f"[-] {token} Dead")
        return f"エラー: {e}"

async def check_tokens(tokens: list):
    alive_tokens = []
    dead_tokens = []
    async with aiohttp.ClientSession() as session:
        tasks = [check_token_status(token, session) for token in tokens]
        results = await asyncio.gather(*tasks)
        for token, result in zip(tokens, results):
            if result == "生存":
                alive_tokens.append(token)
            else:
                dead_tokens.append(token)
    return alive_tokens, dead_tokens

async def main():
    tokens = read_tokens_from_file("result_alt.txt")
    if not tokens:
        print(Fore.RED + "トークンが見つかりません。終了します。")
        return

    alive_tokens, dead_tokens = await check_tokens(tokens)

    with open("alive_tokens.txt", "w", encoding="utf-8") as file:
        for token in alive_tokens:
            file.write(token + "\n")
    print(Fore.GREEN + f"\n生存トークンをalive_tokens.txtに保存しました。合計: {len(alive_tokens)}")

    with open("dead_tokens.txt", "w", encoding="utf-8") as file:
        for token in dead_tokens:
            file.write(token + "\n")
    print(Fore.GREEN + f"死亡トークンをdead_tokens.txtに保存しました。合計: {len(dead_tokens)}")

if __name__ == "__main__":
    asyncio.run(main())
