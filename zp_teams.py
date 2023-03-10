import json
from time import sleep
from zp import ZwiftLogin
from spaces import get_space
import streamlit as st
import pandas as pd
def team_list():
    """Get the list of teams
    https://zwiftpower.com/api3.php?do=team_list
    """
    api_urls = {'teams': "https://zwiftpower.com/api3.php?do=team_list"}
    z = ZwiftLogin()
    results = z.get(api_urls)
    results['teams_df']['riders'] = results['teams_df']['riders'].apply(pd.to_numeric, errors='coerce')
    try:
        fs = get_space()
        with fs.open('zwiftapi/list_teams/list_teams.json', 'w') as f:
            json.dump(results['teams_json'], f)
    except Exception as e:
        print(f"failed to write json: {e}")
    return results

def team_riders(team_id):
    """Get the list of team members
    https://zwiftpower.com/api3.php?do=team_riders&id=2707
    """
    api_url = {'team_riders': f"https://zwiftpower.com/api3.php?do=team_riders&id={team_id}"}
    z = ZwiftLogin()
    results = z.get(api_url)

    return results

def save_record(path, record):
    """
    - f"zwiftapi/team_members/{team_id}.json
    results['members_json']
    """
    try:
        fs = get_space()
        with fs.open(path, 'w') as f:
            json.dump(record, f)
    except Exception as e:
        print(f"Failed to get team members: {e}")

def team_refresh():
    """Refresh the team list and team riders"""
    teams = team_list()
    for t in teams['teams_json']['data']:
        team_riders(t['team_id'])
        sleep(.5)
def team_overlap_by_rider(team_df: pd.DataFrame, include: int = None, depth: int = 20) -> dict:
    riders = {}
    riders_teams = {}
    teams = team_df.iloc[0:depth].to_dict('records') # How many team to look at
    if include is not None:
        teams.update(team_df.iloc[team_df['team_id'] == include].to_dict('records'))
    for t in team_df.iloc[0:depth].to_dict('records'):
        st.write(f"Getting rider list for {t['tln']}")
        members = team_riders(t['team_id'])
        st.write(f"- {t['tln']} as {len(members['team_riders_df'])} members")
        for r in members['team_riders_df'].to_dict('records'):
            if r['zwid'] not in riders.keys():
                riders[r['zwid']] = r
                riders_teams[r['zwid']] = {'zwid': r['zwid'], 'name': r['name'], 'teams': [t['tln']]}
            else:
                # print(riders_teams[r['zwid']]['teams'])
                riders_teams[r['zwid']]['teams'].append(t['tln'])
        sleep(.5)
    dt = pd.DataFrame(riders_teams.values())
    dt['team_count'] = dt.teams.apply(lambda x: len(x))
    return {'riders': riders, 'riders_teams': riders_teams, 'team_overlap': dt}