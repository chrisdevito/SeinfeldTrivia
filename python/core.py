import random
import requests
import collections

from bs4 import BeautifulSoup

import const


def get_season_data():
    """Get season data with each episode

    Returns:
        dict: Dictionary of data
    """

    response = requests.get(const.SEINFELD_SCRIPT, headers=const.headers)
    response.raise_for_status()  # Ensure the request was successful

    # parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    season_tags = soup.find_all("b")

    # get data
    season_dict = collections.defaultdict(dict)
    for season_tag in season_tags:
        season_title = season_tag.get_text(strip=True).replace("\xa0", "")
        if "Season" not in season_title and "Pilot" not in season_title:
            continue

        episode_index = 1
        for episode_tag in season_tag.find_all_next("tr"):
            if episode_tag.find("b"):  # Stop when encountering the next season
                break

            text = episode_tag.get_text(strip=True).replace("\n", "")
            if not text:
                break

            result = const.EPISODE_REGEX.search(text)
            if not result:
                continue

            episode_link_tag = episode_tag.find("a")
            episode_link = (
                episode_link_tag["href"].strip() if episode_link_tag else None
            )
            if not episode_link:
                continue

            episode_name = result.group("episode_name")
            season_result = const.SEASON_REGEX.search(season_title)
            season_number = season_result.group("season_number").strip(" ")
            if season_number == "t":
                season_number = 0
                episode_name = "Good News Bad News/Seinfeld Chronicles"

            airdate = season_result.group("season_airdate")
            if not airdate:
                airdate = season_result.group("season_year")

            season_dict[season_title][episode_name] = {
                "episode_number": result.group("episode_number"),
                "season_number": season_number,
                "season title": season_title,
                "season_episode_number": episode_index,
                "episode_airdate": airdate,
                "site_link": f"https://www.seinfeldscripts.com/{episode_link}",
            }
            episode_index += 1

    return season_dict


def get_random_episode(season_dict=None):
    """Get a random episode of seinfeld

    Args:
        season_dict(dict): dictionary to randomly get values from

    Returns:
        tuple(key, value): The random episode
    """
    season_dict = season_dict or get_season_data()
    season = random.choice(list(season_dict.keys()))
    return random.choice(list(season_dict[season].items()))


def get_script_data(site_link=None):
    """Get script info from site

    Args:
        site_link(str): Link to site to scrape

    Returns:
        list: script per line
    """
    site_link = site_link or r"https://www.seinfeldscripts.com/TheStakeout.htm"
    response = requests.get(
        site_link,
        headers=const.headers,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    script_tags = soup.find_all("p")

    script_lines = []
    start_collecting_script = False
    for script_tag in script_tags:
        text = script_tag.get_text(strip=True)

        if ":" in text:
            start_collecting_script = True

        if start_collecting_script:
            if "[End]" in text or text == "End.":
                break
            script_lines.append(script_tag.get_text(strip=True))

    return script_lines


def get_random_lines(episode_data=None):
    """Get random lines

    Args:
        episode_data(dict): Episode dict

    Returns:
        str: Random lines
    """
    episode_name, episode_info = episode_data or get_random_episode()
    script_lines = get_script_data(episode_info["site_link"])

    script_line = random.choice(script_lines)
    script_size = len(script_lines)
    line_index = script_lines.index(script_line)
    next_line = script_line
    previous_line = script_line
    idx = 1
    prepended_lines = []
    while True and idx < 6:
        if ":" in previous_line:
            break

        previous_index = line_index - idx
        if previous_index < 0:
            break
        previous_line = script_lines[line_index + idx]
        if previous_line:
            prepended_lines.insert(0, previous_line)

        idx += 1

    idx = 1
    appended_lines = []

    while True and idx < 6:
        if next_line.endswith("."):
            break
        next_index = line_index + idx
        if next_index == script_size:
            break

        next_line = script_lines[next_index]
        if next_line:
            appended_lines.append(next_line)

        idx += 1

    return "\n".join(prepended_lines + [script_line] + appended_lines)
