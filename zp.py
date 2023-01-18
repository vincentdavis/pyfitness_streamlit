# import datetime
# import json
# from bs4 import BeautifulSoup
# from requests import Session
# import logging
# logging.basicConfig(filename='fetcher.log', level=logging.ERROR)
from requests_html import HTMLSession
import requests

from datetime import datetime, timedelta
import streamlit as st

def zwiftprofile(username, password):
    try:
        get_token = requests.get(f"https://z00pbp8lig.execute-api.us-west-1.amazonaws.com/latest/zwiftId?username={username}&pw={password}")
        get_profile = requests.get(f"https://zwiftapi.weracehere.org/profile?zid={get_token.json()}")
        return get_profile.json()
    except Exception as e:
        st.write(f"Error:\n{e}.")

class ZwiftLogin(object):
    def __init__(self):
        self.login_data = {}
        self.login_data.update(st.secrets['zwiftpower'])
    def get_request(self, viewurl, content=False):
        session = HTMLSession()
        z = session.get('https://zwiftpower.com')
        # logging.info(z.cookies.get('phpbb3_lswlk_sid'))
        # print(z.cookies)
        self.login_data['sid'] = z.cookies.get('phpbb3_lswlk_sid')
        if "Login Required" in z.text:  # get logged in
            print("Login Required")
            try:
                session.post("https://zwiftpower.com", data=self.login_data)
                assert "Profile" in session.get("https://zwiftpower.com/events.php").text
                # print('login success')
                # logging.info('Login successful')
            except Exception as e:
                print('Login error')
                # logging.error(f"Failed to login: {e}")
        response = session.get(viewurl)
        # logging.info("Status", response.status_code)
        if content:
            return response.content
        else:
            try:
                return response.json()
            except Exception as e:
                print("Error in json", e)
                return response.text
#
# class ZwiftPowerAPI(object):
#     def __init__(self, login_data=None, db_collection=collection):
#         self.db_collection = db_collection
#
#     def dual_regarding(self, id, refresh=False):
#         """
#         Dual Regarding
#         """
#         viewurl = f"https://zwiftpower.com/api3.php?do=set_analysis&set_id={id}"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['dual_regarding'].find({"id": id}).count() >= 1:
#                 is_in_cache = self.db_collection['dual_regarding'].find({"id": id})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 print("Calling api")
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(viewurl)
#                 fts = {'id': id, 'data': [{'data': ftsdata}], 'cached':  'True', 'datetime':  datetime.now()}
#                 self.db_collection['dual_regarding'].insert(fts)
#                 return [fts]
#             except Exception as e:
#                 logging.info(f"dual_regarding error: {e}")
#                 print(e)
#                 return [{}]
#
#     def results_view(self, zid, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         viewurl = f"https://zwiftpower.com/cache3/results/{zid}_view.json"
#         # zwifturl = f"https://zwiftpower.com/cache3/results/{zid}_zwift.json"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['results_view'].find({"zid" : zid}).count() >=1:
#                 is_in_cache = self.db_collection['results_view'].find({"zid" : zid})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(viewurl)
#                 fts_cached = {'zid': zid, 'data': ftsdata['data'], 'cached':  'False'}
#                 fts = {'zid': zid, 'data': ftsdata['data'], 'cached':  'True', 'datetime':  datetime.now()}
#                 self.db_collection['results_view'].insert(fts)
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"fetch_sprints FTS error: {e}")
#                 print(e)
#                 return [{}]
#
#     def results_zwift(self, zid, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         zwifturl = f"https://zwiftpower.com/cache3/results/{zid}_zwift.json"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['results_zwift'].find({"zid" : zid}).count() >=1:
#                 is_in_cache = self.db_collection['results_zwift'].find({"zid" : zid})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(zwifturl)
#                 fts_cached = {'zid': zid, 'data': ftsdata['data'], 'cached':  'False'}
#                 fts = {'zid': zid, 'data': ftsdata['data'], 'cached':  'True', 'datetime':  datetime.now()}
#                 self.db_collection['results_zwift'].insert(fts)
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"fetch_sprints FTS error: {e}")
#                 print(e)
#                 return [{}]
#
#     def fetch_sprints(self, zid, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         ftsurl = f"https://zwiftpower.com/api3.php?do=event_sprints&zid={zid}"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['event_sprints'].find({"zid" : zid}).count() >=1:
#                 is_in_cache = self.db_collection['event_sprints'].find({"zid" : zid})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(ftsurl)
#                 fts_cached = {'zid': zid, 'data': ftsdata['data'], 'cached':  'False'}
#                 fts = {'zid': zid, 'data': ftsdata['data'], 'cached':  'True', 'datetime':  datetime.now()}
#                 self.db_collection['event_sprints'].insert(fts)
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"fetch_sprints FTS error: {e}")
#                 print(e)
#                 return [{}]
#
#     def team_result(self, id, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         ftsurl = f"https://zwiftpower.com/api3.php?do=team_results&id={id}"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['team_result'].find({"id" : id}).count() >=1:
#                 is_in_cache = self.db_collection['team_result'].find({"id" : id})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(ftsurl)
#                 fts_cached = {'id': id, 'data': ftsdata['data'], 'events': ftsdata['events'], 'cached':  'False'}
#                 fts = {'id': id, 'data': ftsdata['data'], 'events': ftsdata['events'], 'cached':  'True', 'datetime':  datetime.now()}
#                 self.db_collection['team_result'].find({"id": id})
#                 if self.db_collection['team_result'].find({"id" : id}).count() >=1:
#                     myquery = {"id": id}
#                     newvalues = {"$set": fts}
#                     self.db_collection['team_result'].update_one(myquery, newvalues)
#                 else:
#                     self.db_collection['team_result'].insert(fts)
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"fetch_sprints FTS error: {e}")
#                 print(e)
#                 return [{}]
#     def fetch_standing(self, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         try:
#             ftsurl = f"https://zwiftpower.com/cache3/lists/2_standings_.json?_=1643631557129"
#             is_in_cache = False
#             if not refresh:
#                 if self.db_collection['standings'].find().count() >= 1:
#                     is_in_cache = self.db_collection['standings'].find().sort('datetime', pymongo.DESCENDING)
#             if is_in_cache:
#                 return is_in_cache
#             else:
#                 try:
#                     zw = ZwiftLogin()
#                     ftsdata = zw.get_request(ftsurl)
#                     standing = {'data': ftsdata['data'], 'cached': 'True', 'datetime': datetime.now()}
#                     self.db_collection['standings'].insert(standing)
#                     return [standing]
#                 except Exception as e:
#                     logging.info(f"fetch_standing error: {e}")
#                     print(e)
#                     return [{}]
#         except Exception as e:
#             print(str(e))
#             return [{}]
#
#     def team_riders(self, id, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         ftsurl = f"https://zwiftpower.com/api3.php?do=team_riders&id={id}&_=1643045203511"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['team_riders'].find({"id": id}).count() >= 1:
#                 is_in_cache = self.db_collection['team_riders'].find({"id": id})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(ftsurl)
#                 fts_cached = {'id': id, 'data': ftsdata['data'], 'cached':  'False',}
#                 fts = {'id': id, 'data': ftsdata['data'], 'cached':  'True', 'datetime':  datetime.now()}
#                 self.db_collection['team_riders'].insert(fts)
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"fetch_sprints FTS error: {e}")
#                 print(e)
#                 return [{}]
#
#     def team_list(self):
#         """
#         Fastest through segment: FTS
#         """
#         try:
#             ftsurl = f"https://zwiftpower.com/api3.php?do=team_list&_=1643046267347"
#             is_in_cache = False
#             time_between_insertion = None
#             if self.db_collection['team_list'].find().count() >= 1:
#                 time_between_insertion = datetime.now() - list(self.db_collection['team_list'].find())[-1].get(
#                     'date_sync')
#             if time_between_insertion is None or time_between_insertion.days > 1:
#                 try:
#                     zw = ZwiftLogin()
#                     ftsdata = zw.get_request(ftsurl)
#                     fts_cached= {'date_sync': datetime.now(), 'data': ftsdata['data'], 'cached':  'False'}
#                     fts = {'date_sync': datetime.now(), 'data': ftsdata['data'], 'cached':  'True', 'datetime':  datetime.now()}
#                     self.db_collection['team_list'].insert(fts)
#                     return [fts_cached]
#                 except Exception as e:
#                     logging.info(f"fetch_sprints FTS error: {e}")
#                     print(e)
#                     return []
#             else:
#                 # print(list(self.db_collection['team_list'].find())[-1])
#                 return self.db_collection['team_list'].find()
#         except Exception as e:
#             print("Exception", str(e))
#             return  []
#
#     def fetch_primes(self, zid, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         ftsurl = f"https://zwiftpower.com/api3.php?do=event_primes&zid={zid}&_=1643043472109"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['event_primes'].find({"zid": zid}).count() >= 1:
#                 is_in_cache = self.db_collection['event_primes'].find({"zid": zid})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(ftsurl)
#                 fts_cached = {'zid': zid, 'data': ftsdata['data'], 'cached':  'False'}
#                 fts = {'zid': zid, 'data': ftsdata['data'], 'cached':  'True', 'datetime':  datetime.now()}
#                 self.db_collection['event_primes'].insert(fts)
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"fetch_sprints FTS error: {e}")
#                 print(e)
#                 return [{}]
#
#     def profile_dual_analysis(self, id, refresh=False):
#         """
#         profile_analysis
#         """
#         url = f"https://zwiftpower.com/cache3/profile/{id}_analysis_list.json"
#         is_in_cache = False
#         if not refresh:
#             try:
#                 if self.db_collection['profile_dual_analysis'].find({"id": id}).count() >= 1:
#                     is_in_cache = self.db_collection['profile_dual_analysis'].find({"id": id})
#             except Exception as e:logging.error(f"profile_dual_analysis error: {e}")
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(url)
#                 fts_cached = {'id': id, 'data': ftsdata['data'], 'cached': 'False'}
#                 fts = {'id': id, 'data': ftsdata['data'], 'cached': 'True', 'datetime': datetime.now(), 'run': False}
#                 try:
#                     self.db_collection['profile_dual_analysis'].insert(fts)
#                 except Exception as e: logging.error(f"profile_dual_analysis error: {e}")
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"profile_dual_analysis error: {e}")
#                 print(e)
#                 return [{}]
#
#     def profile_all(self, zid, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         ftsurl = f"https://zwiftpower.com/cache3/profile/{zid}_all.json"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['profile_all'].find({"zid": zid}).count() >= 1:
#                 is_in_cache = self.db_collection['profile_all'].find({"zid": zid})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(ftsurl)
#                 fts_cached = {'zid': zid, 'data': ftsdata['data'], 'cached': 'False'}
#                 fts = {'zid': zid, 'data': ftsdata['data'], 'cached': 'True', 'datetime': datetime.now()}
#                 self.db_collection['profile_all'].insert(fts)
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"fetch_sprints FTS error: {e}")
#                 print(e)
#                 return [{}]
#
#     def profile_rider_compare_victims(self, zid, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         ftsurl = f"https://zwiftpower.com/cache3/profile/{zid}_rider_compare_victims.json"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['profile_rider_compare_victims'].find({"zid": zid}).count() >= 1:
#                 is_in_cache = self.db_collection['profile_rider_compare_victims'].find({"zid": zid})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(ftsurl)
#                 fts_cached = {'zid': zid, 'data': ftsdata['data'], 'cached': 'False'}
#                 fts = {'zid': zid, 'data': ftsdata['data'], 'cached': 'True', 'datetime': datetime.now()}
#                 self.db_collection['profile_rider_compare_victims'].insert(fts)
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"fetch_sprints FTS error: {e}")
#                 print(e)
#                 return [{}]
#
#     def profile_analysis_list(self, zid, refresh=False):
#         """
#         Fastest through segment: FTS
#         """
#         ftsurl = f"https://zwiftpower.com/cache3/profile/{zid}_rider_compare_victims.json"
#         is_in_cache = False
#         if not refresh:
#             if self.db_collection['profile_analysis_list'].find({"zid": zid}).count() >= 1:
#                 is_in_cache = self.db_collection['profile_analysis_list'].find({"zid": zid})
#         if is_in_cache:
#             return is_in_cache
#         else:
#             try:
#                 zw = ZwiftLogin()
#                 ftsdata = zw.get_request(ftsurl)
#                 fts_cached = {'zid': zid, 'data': ftsdata['data'], 'cached': 'False'}
#                 fts = {'zid': zid, 'data': ftsdata['data'], 'cached': 'True', 'datetime': datetime.now()}
#                 self.db_collection['profile_analysis_list'].insert(fts)
#                 return [fts_cached]
#             except Exception as e:
#                 logging.info(f"fetch_sprints FTS error: {e}")
#                 print(e)
#                 return [{}]
#     def fetch_profile_ext(self, zwid, refresh=False, avatar=True):
#         """
#         Avatar should be false or a path "database/avatar/"
#         """
#         page_url = f"https://zwiftpower.com/profile.php?z={zwid}"
#         zw = ZwiftLogin()
#         page_xml = BeautifulSoup(zw.get_request(page_url, content=True), "lxml")
#         profile_ext = {}
#         try:
#             aurl = page_xml.find("img", {"class": "img-circle"})
#             if aurl:
#                 profile_ext['avatar_url'] = page_xml.find("img", {"class": "img-circle"}).get("src")
#             else:
#                 profile_ext['avatar_url'] = None
#             profile_ext['long_bio'] = page_xml.find(id='long_bio').text if page_xml.find(
#                 id='long_bio') else None
#             profile_ext['zwift_level'] = page_xml.find(
#                 title='Zwift in-game level').text if page_xml.find(title='Zwift in-game level') else None
#             table = page_xml.find("table", id="profile_information")
#             if table:
#                 table_rows = table.find_all("tr")
#                 for tr in table_rows:
#                     td = tr.find_all(["td", "th"])
#                     row = [i.text.strip() for i in td]
#                     # print(row)
#                     if "Country" in row and not row[1][0].isdigit():
#                         profile_ext["country"] = row[1] or None
#                     if "Race Ranking" in row:
#                         profile_ext["race_rank_pts"] = int("".join(c for c in row[1].split(" ")[0] if c.isdigit()))
#                         profile_ext["race_rank_place"] = int(
#                             "".join(c for c in row[1].split(" pts in ")[1] if c.isdigit()))
#                     if "Category" in row:
#                         profile_ext["race_rank_catagory"] = int("".join(c for c in row[1] if c.isdigit()))
#                     if "Age Group" in row:
#                         profile_ext["race_rank_age"] = int("".join(c for c in row[1] if c.isdigit()))
#                     if "Weight Group" in row:
#                         profile_ext["race_rank_weight"] = int("".join(c for c in row[1] if c.isdigit()))
#                     if "Team" in row:
#                         row_test = "".join(c for c in row[1] if c.isdigit())
#                         if row_test.isdigit():
#                             profile_ext["race_rank_team"] = int("".join(c for c in row[1] if c.isdigit()))
#                         else:
#                             profile_ext["race_team"] = row[1] or None
#                     if "Minimum Category" in row:
#                         profile_ext["minimum_category"] = row[1][0] or None
#                         profile_ext["minumun_catagory_female"] = row[1][2] if row[1][2] in ['A', 'B', 'C', 'D',
#                                                                                         'E'] else None
#                         profile_ext['races'] = int("".join(c for c in row[1] if c.isdigit()))
#                     if "Age" in row:
#                         profile_ext["age"] = row[1] or None
#                     if "Average" in row:
#                         profile_ext["average_watts"] = int(row[1].split("watts")[0])
#                         profile_ext["average_wkg"] = float(row[1].split(" /")[1].replace("wkg", ""))
#                     if "FTP" in row:
#                         profile_ext["ftp"] = None
#                         profile_ext["kg"] = None
#                         try:
#                             profile_ext["ftp"] = int(row[1].split("w")[0])
#                             profile_ext["kg"] = int("".join(c for c in row[1].split('~ ')[1] if c.isdigit()))
#                         except Exception as e:
#                             logging.error(f"FTP not found: {e}")
#         except Exception as e:
#             print("Exception", str(e))
#             logging.error(f"fetch_profile_ext error: {e}")
#         try:
#             if avatar:
#                 # database/avatar/
#                 try:
#                     tstamp = datetime.utcnow().isoformat()
#                     file_name = f"avatar_{zwid}_{tstamp}.jpeg"
#                     zw = ZwiftLogin()
#                     avatar_file = zw.get_request(profile_ext['avatar_url'])
#                     # self.db.save_avatar(file_name, avatar_file)
#                 except Exception as e:
#                     logging.error(f"Avatar file save error: {e}")
#                     avatar_file = None
#                 finally:
#                     profile_ext['avatar_file'] = file_name
#         except Exception as e:
#             profile_ext['avatar_file'] = None
#             logging.error(f"fetch_profile_ext AVattar error: {e}")
#         finally:
#             return [{'data': profile_ext}]
#
#     def results_frr(self, zid, refresh=False):
#         """Custom results_view for frr"""
#         results = self.results_view(zid, refresh=refresh)['data']
#         frr = []
#         for r in results:
#             r['dbase id'] = ""
#             r['PEN'] = r['category']
#             r['Pen position'] = r['position_in_cat']
#             r['ZWID'] = r['zwid']
#             r['ZEVENT'] = r['zid']
#             r['Stage Time'] = r['gun_time']
#             r['WATT'] = r['avg_power']
#             if isinstance(r['WATT'], list):
#                 r['WATT'] = r['WATT'][0]
#             else:
#                 r['WATT'] = 0
#             r['NP'] = r['np']
#             if isinstance(r['NP'], list):
#                 r['NP'] = r['NP'][0]
#             else:
#                 r['NP'] = 0
#             r['WKG'] = r['avg_wkg']
#             if isinstance(r['WKG'], list):
#                 r['WKG'] = r['WKG'][0]
#             else:
#                 r['NP'] = 0
#             keep = ['dbase id', 'PEN', 'Pen position', 'ZWID', 'ZEVENT', 'Stage Time', 'WATT', 'NP', 'WKG']
#             frr.append({k:v for k, v in r.items() if k in keep})
#         return frr