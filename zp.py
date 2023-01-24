# import datetime
# from bs4 import BeautifulSoup
import logging
from time import sleep

logging.basicConfig(filename='fetcher.log', level=logging.ERROR)
from requests_html import HTMLSession

import pandas as pd
import streamlit as st
import requests


def zwiftprofile(username, password):
    try:
        get_token = requests.get(
            f"https://z00pbp8lig.execute-api.us-west-1.amazonaws.com/latest/zwiftId?username={username}&pw={password}")
        get_profile = requests.get(f"https://zwiftapi.weracehere.org/profile?zid={get_token.json()}")
        return get_profile.json()
    except Exception as e:
        st.write(f"Error:\n{e}.")


class ZwiftLogin(object):
    def __init__(self):
        self.login_data = {}
        self.login_data.update(st.secrets['zwiftpower'])

    def get(self, api_urls, content=False):
        session = HTMLSession()
        z = session.get('https://zwiftpower.com')
        logging.info(z.cookies.get('phpbb3_lswlk_sid'))
        self.login_data['sid'] = z.cookies.get('phpbb3_lswlk_sid')
        if "Login Required" in z.text:  # get logged in
            try:
                session.post("https://zwiftpower.com", data=self.login_data)
                assert "Profile" in session.get("https://zwiftpower.com/events.php").text
                # print('login success')
                logging.info('Login successful')
            except Exception as e:
                print('Login error')
                logging.error(f"Failed to login: {e}")
            data = {}
            for name, url in api_urls.items():
                response = session.get(url)
                logging.info("Status", response.status_code)
                try:
                    res = response.json()
                    data[f"{name}_json"] = res
                    data[f"{name}_df"] = pd.DataFrame(res['data'])
                except Exception as e:
                    print("Error in json", e)
                    data[f"{name}_json"] = None
                sleep(1)
            return data


def fix_columns(df, col):
    """Fix columns that have a list of data.
    We will use the first value as replacement for the column value and the second as NAME_2"""
    try:
        split_df = pd.DataFrame(df[col].tolist(), columns=[col, f"{col}_2"])
        # concat df and split_df
        df.drop(col, axis=1, inplace=True)
        return pd.concat([df, split_df], axis=1)
    except Exception as e:
        print(f"Problem converting: {col}")
        print(e)
        return df


def event_results(event_url):
    """Get the results of an event.
    Event URLS
    Main event page
        https://zwiftpower.com/cache3/results/3438682_zwift.json
        https://zwiftpower.com/cache3/results/3438682_view.json
    Sprint & KOMs
        https://zwiftpower.com/api3.php?do=event_sprints&zid=3438615
    Primes
        https://zwiftpower.com/api3.php?do=event_primes&zid=3438615
    Power Curve, for event, needs rider ID or get all.
        https://zwiftpower.com/api3.php?do=critical_power_event&zwift_id=507355&zwift_event_id=3438615&type=watts
    Analysis
    https://zwiftpower.com/api3.php?do=analysis_event_list&zwift_event_id=3438615
    """
    try:
        assert "https://zwiftpower.com/events.php?zid=" in event_url
    except AssertionError:
        print("Invalid event URL")
        return None
    # parse url
    event_id = event_url.split("=")[-1].split("&")[0]

    api_urls = dict(view=f"https://zwiftpower.com/cache3/results/{event_id}_view.json",
                    zwift=f"https://zwiftpower.com/cache3/results/{event_id}_zwift.json",
                    sprints=f"https://zwiftpower.com/api3.php?do=event_sprints&zid={event_id}",
                    primes=f"https://zwiftpower.com/api3.php?do=event_primes&zid={event_id}",
                    analysis=f"https://zwiftpower.com/api3.php?do=analysis_event_list&zwift_event_id={event_id}")
    z = ZwiftLogin()
    results = z.get(api_urls)
    for name in results.keys():
        if '_df' in name:
            for c in results[name].columns:
                if isinstance(results[name][c][0], list):
                    results[name] = fix_columns(results[name], c)
    results['event_id'] = event_id
    return results
