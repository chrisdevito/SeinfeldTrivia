import re

SEINFELD_SCRIPT = r"https://www.seinfeldscripts.com/seinfeld-scripts.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
}
EPISODE_REGEX = re.compile(
    r"(?P<episode_number>\d+)(?P<episode_name>.+)(?P<episode_airdate>\(\d+\/\d+\/\d+\))"
)

SEASON_REGEX = re.compile(
    r"(\w+)(?P<season_number>.+)(?P<season_airdate>\(\d+-\d+\))"
)
