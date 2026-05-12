import urllib.request
import urllib.parse
import json
import time
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT = SCRIPT_DIR / "search_results.json"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check likely existing Chinese translation status for a historical English book list."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output JSON path. Defaults to search_results.json next to this script.",
    )
    return parser.parse_args()

books = [
    # Travelogues
    'Through the Heart of Patagonia Hesketh Prichard',
    'A Woman\'s Trek from the Cape to Cairo Mary Hall',
    'The Land of the Black Mountain Reginald Wyon',
    'In the Tail of the Peacock Isabel Savory',
    'The Andes and the Amazon C. Reginald Enock',
    'Alone in West Africa Mary Gaunt',
    'A Girl\'s Ride in Iceland Mrs. Alec-Tweedie',
    'Through the Unknown Pamirs O. Olufsen',
    'A Vagabond in the Caucasus Stephen Graham',
    'A Year in Brazil Hastings Charles Dent',
    'The Land of Footprints Stewart Edward White',
    'The Desert of the Exodus Edward Henry Palmer',
    'From the Cape to Cairo Ewart S. Grogan',
    'Wanderings in South America Charles Waterton',
    'Travels in West Africa Mary Kingsley',
    'Unknown Mexico Carl Lumholtz',
    'The Ruins and Excavations of Ancient Rome Rodolfo Lanciani',
    'Among the Himalayas L.A. Waddell',
    'My Life with the Eskimo Vilhjalmur Stefansson',
    'Tenting on the Plains Elizabeth Bacon Custer',
    # Sci-Fi
    'A Columbus of Space Garrett P. Serviss',
    'The Moon Metal Garrett P. Serviss',
    'The Master Key L. Frank Baum',
    'The Brick Moon Edward Everett Hale',
    'The Blind Spot Austin Hall',
    'City of Endless Night Milo Hastings',
    'The Metal Monster A. Merritt',
    'The Hampdenshire Wonder J. D. Beresford',
    'Olga Romanoff George Griffith',
    'The Angel of the Revolution George Griffith',
    'The Secret of the Earth Charles Willing Beale',
    'A Journey in Other Worlds John Jacob Astor IV',
    'Symzonia A Voyage of Discovery Adam Seaborn',
    'Mizora A Prophecy Mary E. Bradley Lane',
    'The Republic of the Southern Cross Valery Bryusov',
    'Darkness and Dawn George Allan England',
    'The Lord of the Sea M. P. Shiel',
    'Edison\'s Conquest of Mars Garrett P. Serviss',
    'The Centaur Algernon Blackwood',
    'The Hampdenshire Wonder J. D. Beresford'
]

args = parse_args()
results = {}
for book in books:
    query = f'"{book.split(" ")[0]} {book.split(" ")[1]}" (豆瓣 OR 中文版 OR 中译本)'
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        if '豆瓣读书' in html or '中文版' in html or '中译本' in html or '出版' in html:
            results[book] = 'Likely Translated'
        else:
            results[book] = 'No Translation Found'
    except Exception as e:
        results[book] = 'Error: ' + str(e)
    time.sleep(1) # Be nice to DDG

output_path = args.output
if not output_path.is_absolute():
    output_path = (Path.cwd() / output_path).resolve()
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"Done: {output_path}")
