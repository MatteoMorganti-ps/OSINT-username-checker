import requests
from rich import print

username = input("[bold cyan] Inserisci username: [/bold cyan] ")

sites ={
    "Instagram": f"https://www.instagram.com/{username}/",
    "Facebook": f"https://www.facebook.com/{username}",
    "GitHub": f"https://github.com/{username}",
    "Reddit": f"https://www.reddit.com/user/{username}",
    "TikTok": f"https://www.tiktok.com/@{username}"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

for site, url in sites.items():
    try:
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            print(f"[green][+] Trovato su {site}[/green] -> {url}")

        elif response.status_code == 404:
            print(f"[red][-] Non trovato su {site}[/red]")

        else:
            print(f"[yellow][!] Risposta {response.status_code} su {site}[/yellow]")
    
    except:
        print(f"[red][!] Errore su {site}[/bold red] -> {e}")