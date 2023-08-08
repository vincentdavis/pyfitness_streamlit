# import datetime
# from bs4 import BeautifulSoup
import json
import logging
from time import sleep

# logging.basicConfig(filename='zp.log', level=logging.ERROR)
from requests_html import HTMLSession


import pandas as pd
import streamlit as st

# import s3fs
import requests


def zwiftprofile(username, password):
    try:
        get_token = requests.get(
            f"https://z00pbp8lig.execute-api.us-west-1.amazonaws.com/latest/zwiftId?username={username}&pw={password}"
        )
        get_profile = requests.get(f"https://zwiftapi.weracehere.org/profile?zid={get_token.json()}")
        return get_profile.json()
    except Exception as e:
        st.write(f"Error:\n{e}.")


class ZwiftLogin(object):
    def __init__(self):
        self.login_data = {}
        self.login_data.update(st.secrets["zwiftpower"])

    def get(self, api_urls: dict, content=False) -> dict:
        session = HTMLSession()
        z = session.get("https://zwiftpower.com")
        # logging.info(z.cookies.get('phpbb3_lswlk_sid'))
        self.login_data["sid"] = z.cookies.get("phpbb3_lswlk_sid")
        if "Login Required" in z.text:  # get logged in
            try:
                session.post("https://zwiftpower.com", data=self.login_data)
                assert "Profile" in session.get("https://zwiftpower.com/events.php").text
                # print('login success')
                # logging.info('Login successful')
            except Exception as e:
                print("Login error")
                # logging.error(f"Failed to login: {e}")
            data = {}
            for name, url in api_urls.items():
                response = session.get(url)
                # logging.info("Status", response.status_code)
                try:
                    res = response.json()
                    data[f"{name}_json"] = res
                    data[f"{name}_df"] = pd.DataFrame(res["data"])
                except Exception as e:
                    print("Error in json", e)
                    data[f"{name}_json"] = None
                sleep(1)
            return data


def fix_columns(df, col):
    """Fix columns that have a list of data.
    We will use the first value as replacement for the column value and the second as NAME_2
    """
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

    api_urls = dict(
        view=f"https://zwiftpower.com/cache3/results/{event_id}_view.json",
        zwift=f"https://zwiftpower.com/cache3/results/{event_id}_zwift.json",
        sprints=f"https://zwiftpower.com/api3.php?do=event_sprints&zid={event_id}",
        primes=f"https://zwiftpower.com/api3.php?do=event_primes&zid={event_id}",
        analysis=f"https://zwiftpower.com/api3.php?do=analysis_event_list&zwift_event_id={event_id}",
    )
    z = ZwiftLogin()
    results = z.get(api_urls)
    print(results.keys())
    for name in results.keys():
        if "_df" in name:
            for c in results[name].columns:
                if isinstance(results[name][c][0], list):
                    results[name] = fix_columns(results[name], c)
            if "zwid" in results[name].columns:
                results[name]["zwid"] = results[name]["zwid"].astype(str)
    results["frr_df"] = results_frr(results["view_df"], results["zwift_df"])
    results["event_id"] = event_id

    return results


def racer_results(event_url):
    """Get the results of an event.
    https://zwiftpower.com/profile.php?z=
    User profile URLS
    Main uprofile page
        https://zwiftpower.com/cache3/profile/110649_all.json
        https://zwiftpower.com/cache3/profile/110649_rider_compare_victims.json
    Power Curve
        https://zwiftpower.com/api3.php?do=critical_power_profile&zwift_id=110649&zwift_event_id=&type=watts
    ZPoints:
        https://zwiftpower.com/api3.php?do=profile_zpoints&z=110649
        https://zwiftpower.com/api3.php?do=profile_zpoints_power&z=110649
    Courses:
        https://zwiftpower.com/api3.php?do=course_records&z=110649
    """
    try:
        assert "https://zwiftpower.com/profile.php?z" in event_url
    except AssertionError:
        print("Invalid event URL")
        return None
    # parse url
    profile_id = event_url.split("=")[-1].split("&")[0]

    api_urls = dict(
        results=f"https://zwiftpower.com/cache3/profile/{profile_id}_all.json",
        compare=f"https://zwiftpower.com/cache3/profile/{profile_id}_rider_compare_victims.json",
        sprints=f"https://zwiftpower.com/api3.php?do=critical_power_profile&zwift_id={profile_id}&zwift_event_id=&type=watts",
        zpoints=f"https://zwiftpower.com/api3.php?do=profile_zpoints&z={profile_id}",
        zpoints_power=f"https://zwiftpower.com/api3.php?do=profile_zpoints_power&z={profile_id}",
        courses=f"https://zwiftpower.com/api3.php?do=course_records&z={profile_id}",
    )

    z = ZwiftLogin()
    results = z.get(api_urls)
    for name in results.keys():
        if "_df" in name:
            for c in results[name].columns:
                if isinstance(results[name][c][0], list):
                    results[name] = fix_columns(results[name], c)
    results["profile_id"] = profile_id
    return results


def results_frr(view_results: pd.DataFrame, zwift_results: pd.DataFrame) -> pd.DataFrame:
    """Custom results_view for frr input view_results and zwift_results json data"""
    view_results = view_results.copy()
    view_results["id"] = ""
    zwift_results = zwift_results.copy()
    zwift_results.drop(
        columns=[c for c in zwift_results.columns if c not in ["name", "zwid"]],
        inplace=True,
    )
    zwift_results.rename(
        columns={
            "name": "ZWIFT_NAME",
        },
        inplace=True,
    )
    results = view_results.merge(zwift_results, on="zwid", how="left")
    results.rename(
        columns={
            "zid": "ZEVENT",
            "zwid": "ZWID",
            "category": "PEN",
            "position_in_cat": "Pen position",
            "time_gun": "Stage Time",
            "avg_power": "WATT",
            "np": "NP WATT",
            "avg_wkg": "WKG",
            "name": "VIEW_NAME",
        },
        inplace=True,
    )
    keep = [
        "PEN",
        "Pen position",
        "ZWID",
        "ZEVENT",
        "Stage Time",
        "WATT",
        "NP WATT",
        "WKG",
        "id",
        "VIEW_NAME",
        "ZWIFT_NAME",
    ]
    results.drop(columns=[c for c in results.columns if c not in keep], inplace=True)
    return results
