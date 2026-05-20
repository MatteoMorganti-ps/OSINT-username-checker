import csv
import requests
import time

from concurrent.futures import ThreadPoolExecutor

from rich.console import Console
from rich.table import Table

console = Console()

username = input("Enter username: ")

sites = {
    "GitHub": f"https://github.com/{username}",
    "Reddit": f"https://www.reddit.com/user/{username}",
    "TikTok": f"https://www.tiktok.com/@{username}",
    "Instagram": f"https://www.instagram.com/{username}/",
    "Facebook": f"https://www.facebook.com/{username}"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

table = Table(title=f"OSINT Username Scan: {username}")

table.add_column("Platform", style="cyan")
table.add_column("Status", style="bold")
table.add_column("URL", style="green")

start_time = time.time()

scan_results = []


def check_site(site_data):

    site, url = site_data

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            status = "FOUND"

        elif response.status_code == 404:
            status = "NOT FOUND"

        else:
            status = str(response.status_code)

    except Exception:
        status = "ERROR"

    return (site, status, url)


with ThreadPoolExecutor(max_workers=5) as executor:

    results = executor.map(
        check_site,
        sites.items()
    )

    for result in results:

        site, status, url = result

        scan_results.append((site, status, url))
        
        if status == "FOUND":
            display_status = "[green]FOUND[/green]"

        elif status == "NOT FOUND":
            display_status = "[red]NOT FOUND[/red]"

        else:
            display_status = f"[yellow]{status}[/yellow]"

        table.add_row(site, display_status, url)

with open(
    "results.csv",
    mode="w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Platform",
        "Status",
        "URL"
    ])

    writer.writerows(scan_results)

end_time = time.time()

console.print(table)

console.print(
    f"\n[bold cyan]Scan completed in "
    f"{end_time - start_time:.2f} seconds[/bold cyan]"
)