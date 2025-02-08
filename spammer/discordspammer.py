import asyncio
import aiohttp
import random
from colorama import init, Fore

init(autoreset=True)

def read_tokens_from_file(file_path: str) -> list:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = file.read().splitlines()
        print(Fore.GREEN + "[+] トークンの読み込みに成功しました。")
        return tokens
    except FileNotFoundError:
        print(Fore.RED + f"[-] エラー: {file_path} が見つかりません。")
        return []

def read_message_from_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            message = file.read()
        print(Fore.GREEN + "[+] メッセージの読み込みに成功しました。")
        return message
    except FileNotFoundError:
        print(Fore.RED + f"[-] エラー: {file_path} が見つかりません。")
        return ""

def randomMention(userIds):
    userId = random.choice(userIds)
    return f"<@{userId}>"

async def send_message_async(token: str, channelId: str, message: str, proxy: str):
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": token,
        "cache-control": "no-cache",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://discord.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": f"https://discord.com/channels/{channelId}",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "ja",
        "x-discord-timezone": "Asia/Tokyo",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImphLUpQIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMxLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cuZ29vZ2xlLmNvbSIsInNlYXJjaF9lbmdpbmUiOiJnb29nbGUiLCJyZWZlcnJlcl9jdXJyZW50IjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiJ3d3cuZ29vZ2xlLmNvbSIsInNlYXJjaF9lbmdpbmVfY3VycmVudCI6Imdvb2dsZSIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjM0ODk4MSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }
    data = {
        "content": append_random_emoji(message),
        "tts": False,
    }
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"https://discord.com/api/v9/channels/{channelId}/messages", headers=headers, json=data, proxy=proxies.get('http') if proxies else None) as response:
                if response.status == 429:  # Too Many Requests
                    print(Fore.YELLOW + "[*] リクエストが多すぎます。2秒待機して再試行します。")
                    await asyncio.sleep(2)
                    async with session.post(f"https://discord.com/api/v9/channels/{channelId}/messages", headers=headers, json=data, proxy=proxies.get('http') if proxies else None) as retry_response:
                        retry_response.raise_for_status()
                        print(Fore.GREEN + "[+] メッセージ送信に成功しました。")
                else:
                    response.raise_for_status()
                    print(Fore.GREEN + "[+] メッセージ送信に成功しました。")
        except aiohttp.ClientError as e:
            print(Fore.RED + f"[-] トークン {token} でのメッセージ送信に失敗しました: {e}")
            print(Fore.YELLOW + "[*] プロキシなしで再試行します。")
            try:
                async with session.post(f"https://discord.com/api/v9/channels/{channelId}/messages", headers=headers, json=data) as response:
                    if response.status == 429:  # Too Many Requests
                        print(Fore.YELLOW + "[*] リクエストが多すぎます。2秒待機して再試行します。")
                        await asyncio.sleep(2)
                        async with session.post(f"https://discord.com/api/v9/channels/{channelId}/messages", headers=headers, json=data) as retry_response:
                            retry_response.raise_for_status()
                            print(Fore.GREEN + "[+] メッセージ送信に成功しました。")
                    else:
                        response.raise_for_status()
                        print(Fore.GREEN + "[+] メッセージ送信に成功しました。")
            except aiohttp.ClientError as e:
                print(Fore.RED + f"[-] トークン {token} でのメッセージ送信に失敗しました: {e}")

def append_random_emoji(message: str) -> str:
    emojis = [
        "😊", "😂", "😍", "😎", "😢", "😡", "😱", "😴", "😇", "🤔", "🥳", "🤩", "😜", "😋", "😏", "😬", "🤯", "😵", "🤗", "😷",
        "😃", "😄", "😁", "😆", "😅", "🤣", "😌", "😉", "🙃", "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🥸", "🤩",
        "🥳", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣", "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬",
        "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗", "🤔", "🤭", "🤫", "🤥", "😶", "😐", "😑", "😬", "🙄", "😯",
        "😦", "😧", "😮", "😲", "🥱", "😴", "🤤", "😪", "😵", "🤐", "🥴", "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤑", "🤠", "😈",
        "👿", "👹", "👺", "🤡", "💩", "👻", "💀", "☠️", "👽", "👾", "🤖", "🎃", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿",
        "😾", "🙈", "🙉", "🙊", "💋", "💌", "💘", "💝", "💖", "💗", "💓", "💞", "💕", "💟", "❣️", "💔", "❤️", "🧡", "💛", "💚",
        "💙", "💜", "🤎", "🖤", "🤍", "💯", "💢", "💥", "💫", "💦", "💨", "🕳️", "💣", "💬", "👁️‍🗨️", "🗨️", "🗯️", "💭", "💤"
    ]
    random_emoji = random.choice(emojis)
    return f"{message} [{random_emoji}]"

async def main():
    tokens = read_tokens_from_file("token.txt")
    if not tokens:
        print(Fore.RED + "[-] トークンが見つかりません。終了します。")
        return
    channelIds = input(Fore.CYAN + "[*] チャンネルIDをカンマ区切りで入力してください: ").split(',')
    userIds = input(Fore.CYAN + "[*] ユーザーIDをカンマ区切り.ないならn(@everyoneになります): ")
    message = read_message_from_file("message.txt")
    if userIds == "n":
        message += "\n@everyone"
    else:
        userIds = userIds.split(",")
    print(Fore.GREEN + f"[+] メッセージの送信を開始します\nトークンの総数: {len(tokens)}")
    try:
        while True:
            tasks = []
            async with aiohttp.ClientSession() as session:
                for i, token in enumerate(tokens):
                    channelId = channelIds[i % len(channelIds)]
                    userId = random.choice(userIds) if userIds != "n" else None
                    message_to_send = message + randomMention(userIds) if userId else message
                    tasks.append(send_message_async(token=token, channelId=channelId, message=message_to_send, proxy=None))
                    await asyncio.sleep(0.1)
                await asyncio.gather(*tasks)
            print(Fore.GREEN + "[+] OK")
    except KeyboardInterrupt:
        print(Fore.YELLOW + "[*] プログラムが中断されました。")

if __name__ == "__main__":
    asyncio.run(main())
