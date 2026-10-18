import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone

DATA_FILE = "opportunities.json"

SOURCES = [
    {
        "name": "FaucetPay",
        "url": "https://faucetpay.io/",
        "type": "Payment platform",
        "note": "Check supported coins and official API documentation."
    },
    {
        "name": "FreeBitcoin",
        "url": "https://freebitco.in/",
        "type": "Faucet",
        "note": "Check current availability and withdrawal conditions."
    }
]

def check_website(url):
    """Check whether a website responds; this does not verify legitimacy."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CryptoHunter/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return {
                "online": True,
                "status": response.status
            }
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        return {
            "online": False,
            "error": str(error)[:200]
        }

def main():
    results = []

    for source in SOURCES:
        result = {
            **source,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "check": check_website(source["url"])
        }
        results.append(result)

        status = "ONLINE" if result["check"]["online"] else "UNAVAILABLE"
        print(f'{source["name"]}: {status}')

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(results)} website checks to {DATA_FILE}")

if __name__ == "__main__":
    main()
