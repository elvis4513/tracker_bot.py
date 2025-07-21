import requests
from bs4 import BeautifulSoup

def get_windrawwin_tips(date_range):
    url = "https://www.windrawwin.com/tips/"
    tips = []

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select(".tipsTable tbody tr")

        for row in rows:
            try:
                date = row.select_one(".date").text.strip()
                home = row.select_one(".teamHome").text.strip()
                away = row.select_one(".teamAway").text.strip()
                match = f"{home} vs {away}"

                prediction = row.select_one(".tip").text.strip()
                confidence_text = row.select_one(".conf").text.strip().replace('%','')
                confidence = int(confidence_text) if confidence_text else 70

                if date in date_range:
                    tips.append({
                        "date": date,
                        "match": match,
                        "market": "1X2",
                        "prediction": prediction,
                        "confidence": confidence,
                        "source": "Windrawwin"
                    })

                    if "BTTS" in prediction or "Yes" in prediction:
                        tips.append({
                            "date": date,
                            "match": match,
                            "market": "BTTS",
                            "prediction": "Yes",
                            "confidence": confidence,
                            "source": "Windrawwin"
                        })
            except:
                continue
    except Exception as e:
        print("Windrawwin error:", e)

    return tips
