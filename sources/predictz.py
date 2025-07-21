import requests
from bs4 import BeautifulSoup

def get_predictz_tips(date_range):
    url = "https://www.predictz.com/predictions/"
    tips = []

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        rows = soup.select(".match-tips .match-row")

        for row in rows:
            try:
                date = row.select_one(".date").text.strip()
                match = row.select_one(".team-name").text.strip()
                market = "1X2"
                prediction = row.select_one(".pred").text.strip()
                confidence = int(row.select_one(".predconf").text.strip('%'))

                if date in date_range:
                    tips.append({
                        "date": date,
                        "match": match,
                        "market": market,
                        "prediction": prediction,
                        "confidence": confidence,
                        "source": "PredictZ"
                    })
            except:
                continue
    except Exception as e:
        print("PredictZ error:", e)

    return tips
