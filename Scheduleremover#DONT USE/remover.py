import asyncio
import aiohttp
from colorama import init, Fore
import requests

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

def fetch_scheduled_eventsV2(token, server_id):
    url = f"https://discord.com/api/v9/users/@me/scheduled-events?guild_ids={server_id}"
    headers = {
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": token,
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": f"https://discord.com/channels/{server_id}",
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
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImphLUpQIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMxLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tLz9kaXNjb3JkdG9rZW49TVRJNE56azNNams0TVRrMk16ZzROalkwTWcuR3RRc3NGLmpIQUF1emlUem50OTZxVHlGSTdBVXBrMjRpeHF0Y0x1bXdXa1JnIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6Imh0dHBzOi8vZGlzY29yZC5jb20vP2Rpc2NvcmR0b2tlbj1NVE14TVRZeE9UUTRNemd6TlRnek1ESTVOQS5HeXlScG4uRE5YYzJfOGE2a1pySFI5TEtHaENuVFVLNVN5QnJnTVNkcy04ZlkiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiJkaXNjb3JkLmNvbSIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjM1MTY2MiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json()
        event_ids = [event["guild_scheduled_event_id"] for event in events]
        return event_ids
    else:
        print(f"[-] イベントの取得に失敗しました: {response.status_code}")
        return None

async def end_schedule_async(token: str, server_id: str, event_id: str, proxy: str = None):
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
        "referer": f"https://discord.com/channels/{server_id}",
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
        "is_canceled": True
    }
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None
    async with aiohttp.ClientSession() as session:
        try:
            async with session.patch(f"https://discord.com/api/v9/guilds/{server_id}/scheduled-events/{event_id}", headers=headers, json=data, proxy=proxies.get('http') if proxies else None) as response:
                if response.status == 429:  # Too Many Requests
                    print(Fore.YELLOW + "[*] リクエストが多すぎます。5秒待機して再試行します。")
                    await asyncio.sleep(5)
                    async with session.patch(f"https://discord.com/api/v9/guilds/{server_id}/scheduled-events/{event_id}", headers=headers, json=data, proxy=proxies.get('http') if proxies else None) as retry_response:
                        retry_response.raise_for_status()
                        print(Fore.GREEN + "[+] イベント削除に成功しました。")
                else:
                    response.raise_for_status()
                    print(Fore.GREEN + "[+] イベント削除に成功しました。")
        except aiohttp.ClientError as e:
            print(Fore.RED + f"[-] トークン {token} でのイベント削除に失敗しました: {e}")
            print(Fore.YELLOW + "[*] プロキシなしで再試行します。")
            try:
                async with session.patch(f"https://discord.com/api/v9/guilds/{server_id}/scheduled-events/{event_id}", headers=headers, json=data) as response:
                    if response.status == 429:  # Too Many Requests
                        print(Fore.YELLOW + "[*] リクエストが多すぎます。5秒待機して再試行します。")
                        await asyncio.sleep(5)
                        async with session.patch(f"https://discord.com/api/v9/guilds/{server_id}/scheduled-events/{event_id}", headers=headers, json=data) as retry_response:
                            retry_response.raise_for_status()
                            print(Fore.GREEN + "[+] イベント削除に成功しました。")
                    else:
                        response.raise_for_status()
                        print(Fore.GREEN + "[+] イベント削除に成功しました。")
            except aiohttp.ClientError as e:
                print(Fore.RED + f"[-] トークン {token} でのイベント削除に失敗しました: {e}")

async def main():
    tokens = read_file("token.txt").splitlines()
    if not tokens:
        print(Fore.RED + "[-] トークンが見つかりません。終了します。")
        return
    server_id = input(Fore.CYAN + "[*] サーバーIDを入力してください: ")
    print(tokens[0])
    event_ids = fetch_scheduled_eventsV2(token=tokens[0], server_id=server_id)
    if event_ids == []:
        print(Fore.RED + "[-] イベントの取得に失敗しました。終了します。") #サーバーに参加してないToken、またはイベントの管理権限がないToken
        return
    print(event_ids)
    print(Fore.GREEN + f"[+] {len(event_ids)}個のイベント削除を開始します\nトークンの総数: {len(tokens)}")
    try:
        for token in tokens:
            for event_id in event_ids:
                await end_schedule_async(token=token, server_id=server_id, event_id=event_id)
                await asyncio.sleep(0.5)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "[*] プログラムが中断されました。")

if __name__ == "__main__":
    asyncio.run(main())
