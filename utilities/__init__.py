import logging, requests, random, json, re, os
from datetime import datetime, timedelta
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def get_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def get_response(session, url):
    response = session.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )
logger = logging.getLogger()


def generate_cards(players: int, match_id: str) -> dict:
    try:
        os.makedirs('static', exist_ok=True)
        with open('static/local.json', 'r') as file:
            data: dict = json.load(file)
            timestamp = data.get('timestamp')
            age = datetime.now() - datetime.fromtimestamp(timestamp)
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        logger.warning("Card cache is missing or corrupted.")
        age = timedelta(days=999)
    
    if age < timedelta(days=3):
        logger.info(f"Using cached card data for match {match_id}.")
        cardpool = data.get('cards')
        
    else:
        logger.warning("Fetching fresh data...")
        url = 'https://api.scryfall.com/cards/search?q=(game%3Apaper+or+game%3Amtgo)+r%3Au+(t%3Acreature+or+t%3Abackground)+unique%3Acards+-border%3Asilver'
        session = get_session()
        cardpool = []
        page = 1
        while url:
            try:
                logger.info(f"Fetching page {page}")
                response = get_response(session, url)
                cardpool.extend(response['data'])
                logger.info(f"Retrieved {len(response['data'])} cards (total: {len(cardpool)})")
                url = response.get('next_page')
                page += 1
            except Exception as e:
                logger.error(f"Failed to fetch page {page}: {e}")
                return None
        data = {
            'timestamp': datetime.now().timestamp(),
            'cards': cardpool
        }
        with open('static/local.json', 'w') as file:
            json.dump(data, file)
    
    weights = [10 if len(card.get('color_identity', [])) >= 2 else 1 for card in cardpool]    
    cards = {}
    partner_cards = [card for card in cardpool if "Partner" in card.get("keywords", [])]
    for i in range(1, players + 1):
        card = random.choices(cardpool, weights=weights, k=1)[0]

        if "Partner" in card.get("keywords", []):
            # Pick a second partner that is not the same as the first
            second_options = [c for c in partner_cards if c["id"] != card["id"]]
            if second_options:
                partner2 = random.choice(second_options)
                cards[i] = [card, partner2]
            else:
                cards[i] = [card]  # fallback: only one available
        else:
            cards[i] = [card]
    return cards
