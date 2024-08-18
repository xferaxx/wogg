import random
import requests


# Function to get the USD to ILS conversion rate and calculate the interval
def get_money_interval(level):
    try:
        url = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_T6vzCLn8CRQtp5bgxcj3jH0o05MWxxrrn01VAN7g"
        resp = requests.get(url)
        data = resp.json()
        usd = random.randint(1, 100)
        usd_ils = (data["data"]["ILS"]) * usd
        print(f"API Call Success: USD = {usd}, USD in ILS = {usd_ils}")
        return usd, usd_ils
    except Exception as e:
        print(f"Error in get_money_interval: {e}")
        return None, None


# Function to compare the user's guess with the correct value
def compare_resultss(user_guess, usd_ils, level):
    dev = 10 - level  # Deviation allowed decreases with higher levels
    diff = abs(usd_ils - user_guess)
    if diff <= dev:
        return True, usd_ils
    else:
        return False, usd_ils
