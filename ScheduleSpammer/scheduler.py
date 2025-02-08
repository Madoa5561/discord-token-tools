import asyncio
import aiohttp
import random
from colorama import init, Fore
from datetime import datetime, timedelta

init(autoreset=True)

def read_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        print(Fore.GREEN + f"[+] {file_path} の読み込みに成功しました。")
        return content
    except FileNotFoundError:
        print(Fore.RED + f"[-] エラー: {file_path} が見つかりません。")
        return ""

def generate_current_and_future_time():
    now = datetime.utcnow()
    one_year_later = now + timedelta(days=365)
    current_time_str = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    future_time_str = one_year_later.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return current_time_str, future_time_str

async def schedule_async(token: str, serverId: str, location: str, name: str, description: str, proxy: str = None):
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
        "referer": f"https://discord.com/channels/{serverId}",
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
    current_time, future_time = generate_current_and_future_time()
    data = {
        "name": name, #100文字までOK
        "description": description, #1000文字までOK
        "privacy_level": 2,
        "scheduled_start_time": current_time,
        "scheduled_end_time": future_time,
        "entity_type": 3,
        "channel_id": None,
        "entity_metadata": {
            "location": location #100文字までOK
        },
        "broadcast_to_directory_channels": False,
        "recurrence_rule": {
            "start": current_time,
            "frequency": 3,
            "interval": 1,
            "by_weekday": [6, 0, 1, 2, 3],
            "by_month": None,
            "by_month_day": None,
            "by_year_day": None,
            "count": None
        }
    }
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"https://discord.com/api/v9/guilds/{serverId}/scheduled-events", headers=headers, json=data, proxy=proxies.get('http') if proxies else None) as response:
                if response.status == 429:  # Too Many Requests
                    print(Fore.YELLOW + "[*] リクエストが多すぎます。20秒待機して再試行します。")
                    await asyncio.sleep(20)
                    async with session.post(f"https://discord.com/api/v9/guilds/{serverId}/scheduled-events", headers=headers, json=data, proxy=proxies.get('http') if proxies else None) as retry_response:
                        retry_response.raise_for_status()
                        print(Fore.GREEN + "[+] イベント投稿に成功しました。")
                else:
                    response.raise_for_status()
                    print(Fore.GREEN + "[+] イベント投稿に成功しました。")
        except aiohttp.ClientError as e:
            print(Fore.RED + f"[-] トークン {token} でのイベント投稿に失敗しました: {e}")
            print(Fore.YELLOW + "[*] プロキシなしで再試行します。")
            try:
                async with session.post(f"https://discord.com/api/v9/guilds/{serverId}/scheduled-events", headers=headers, json=data) as response:
                    if response.status == 429:  # Too Many Requests
                        print(Fore.YELLOW + "[*] リクエストが多すぎます。10秒待機して再試行します。")
                        await asyncio.sleep(10)
                        async with session.post(f"https://discord.com/api/v9/guilds/{serverId}/scheduled-events", headers=headers, json=data) as retry_response:
                            retry_response.raise_for_status()
                            print(Fore.GREEN + "[+] イベント投稿に成功しました。")
                    else:
                        response.raise_for_status()
                        print(Fore.GREEN + "[+] イベント投稿に成功しました。")
            except aiohttp.ClientError as e:
                print(Fore.RED + f"[-] トークン {token} でのイベント投稿に失敗しました: {e}")

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
    tokens = read_file("token.txt").splitlines()
    if not tokens:
        print(Fore.RED + "[-] トークンが見つかりません。終了します。")
        return
    serverId = input(Fore.CYAN + "[*] サーバーIDを入れてください: ")
    location = read_file("location.txt")
    name = read_file("name.txt")
    description = read_file("description.txt")

    name_max_length = 100  # nameの最大文字数
    location_max_length = 100  # locationの最大文字数
    description_max_length = 1000  # descriptionの最大文字数
    emoji_length = 3  # 絵文字の長さを考慮

    if len(location) >= location_max_length:
        location = location[:location_max_length - emoji_length]
    if len(name) >= name_max_length:
        name = name[:name_max_length - emoji_length]
    if len(description) >= description_max_length:
        description = description[:description_max_length - emoji_length]
    
    print(Fore.GREEN + f"[+] イベントのスケジュールを開始します\nトークンの総数: {len(tokens)}")
    try:
        while True:
            tasks = []
            for token in tokens:
                templocation = append_random_emoji(location)
                tempname = append_random_emoji(name)
                tempdescription = append_random_emoji(description)
                tasks.append(schedule_async(token=token, serverId=serverId, location=templocation, name=tempname, description=tempdescription))
                await asyncio.sleep(0.1)
            await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "[*] プログラムが中断されました。")

if __name__ == "__main__":
    asyncio.run(main())
