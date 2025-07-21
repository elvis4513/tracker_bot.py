import requests
from bs4 import BeautifulSoup

def get_forebet_tips(date_range):
    url = "https://www.forebet.com/en/football-predictions"
    tips = []

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("table.forebet .rcnt tr")

        for row in rows:
            try:
                date_cell = row.select_one(".date_bah")
                if not date_cell:
                    continue
                date = date_cell.text.strip().split()[0]
                match_cell = row.select_one(".homeTeam")
                away_cell = row.select_one(".awayTeam")
                pred_cell = row.select_one(".forepr")
                goal_cell = row.select_one(".fpr2")

                match = f"{match_cell.text.strip()} vs {away_cell.text.strip()}"
                prediction = pred_cell.text.strip()
                confidence = 80 if prediction else 0  # default if not shown

                if date in date_range:
                    tips.append({
                        "date": date,
                        "match": match,
                        "market": "1X2",
                        "prediction": prediction,
                        "confidence": confidence,
                        "source": "Forebet"
                    })

                    # Add Over 2.5 Goals tip if predicted goals > 2.5
                    try:
                        goals = float(goal_cell.text.strip())
                        if goals > 2.5:
                            tips.append({
                                "date": date,
                                "match": match,
                                "market": "Over 2.5",
                                "prediction": "Yes",
                                "confidence": int(min(goals * 30, 95)),
                                "source": "Forebet"
                            })
                    except:
                        continue
            except:
                continue
    except Exception as e:
        print("Forebet error:", e)

    return tips
