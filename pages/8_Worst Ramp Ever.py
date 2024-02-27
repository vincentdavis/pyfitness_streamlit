import streamlit as st

from ramp_test import make_zwo_from_ramp, ramp_test_activity

st.set_page_config(
    page_title="Worst Ramp Ever",
    page_icon="\u1F6B2",
    layout="wide",
    initial_sidebar_state="auto",
)

"""
## The Worst Ramp Test Ever
Questions, comments, contact me on discord: [Vincent.Davis](discordapp.com/users/vincent.davis)

The goal of this project was to take a riders power curve, sometimes called critical power curve and build a workout 
that will produce the that power curve. My initial question was, "Can I build a 20min workout that will produce my 20min 
power profile?" The answer is yes.

As you can image, a 20min workout that will producce your 20min profile, is never going to be easy. What this looks like 
will surprise you.

### How the problem is solved:
1. Define a power profile, it must start with 1 second power and end with 20min and contain as many intermidiat points 
are desired. Something like: `(sec, power) (1, 1000), (2, 900) (3, 875), (5, 800), (30, 500), (60, 450), (300, 400), (1200, 350)`
2. Interperlate the power profile for each second. Keep in mind, (5, 800) means 800 watts(average) for 5 seconds.
3. We are now ready to calculate the workout.

### The workout:
1. We start from the end of the workout and work toward the start.
2. The end power, last second, of the workout will be the riders 1 sec critical power = 1000.
3. The next (second to last) will need to statisfy (1000w + x)/2sec = 900w. x = 800w To make sense of this, if you did 
1000w for 1 second than to have a 2 second average power of 900watts, you only need to do 800watts for the second, 
second.
4. The third is than, (1000w + 800w + x)/3sec = 875w. x = 825w
5. Continue this process until the workout is complete.
6. Now we have ramp power defined for each second of duration from 1-1200seconds
7. The last 30seconds is a 1 second ramp.
8. Average the power for the second to last 30seconds. as a segment. 
9. The first 19min is converted to 1min segments set the the everage power for each segment.

### Corner cases:
. This calculation will sometimes result in the need to do negative power. The power is set to 0 in these cases. Usually 
it is only slightly negative.
. The per second ramp power workout should exactly match the critical power profile if ridden. (except for this issue above)
. The workout created with the 1min segments, is a close approximation of the critical power profile.

## Get a workout:
. Zwift workouts are defined as a % of ftp. You will get 3 workouts,
  . ftp = The value you define below will be used to override your zwift value during the workout.
  . ftp = 1. In the case the workout will define the power you must ride, i.e. 120% of ftp == 120watts. Kinda a hack to 
  set the watts.
  . ftp = user (zwift) defined ftp. The workout will be defined as a % the provided ftp but when you ride it will use 
  your zwift ftp.
. You can define as many (second, watts) points as you like. Starting with 1sec and ending with 1200sec.(20min) or more.
. Result: 4 files, the 3 workouts and the full data as a csv file.
"""

with st.form(key="ramp_test"):
    st.markdown("#### Rider Profile")
    name = st.text_input("Name", value="John and Jill")
    ftp = st.number_input("FTP", min_value=10.0, max_value=1000.0, value=250.0)
    st.markdown("##### Profile")
    prof = st.text_area(
        label="Profile [sec, watts]", value="1, 1000\n5, 800\n30, 500\n60, 450\n300, 400\n1200, 350", height=200
    )
    submit = st.form_submit_button("Submit")

if submit:
    with st.spinner("Processing..."):
        profile = prof.split("\n")
        profile = [x.split(",") for x in profile]
        profile = [(int(x[0]), int(x[1])) for x in profile]
        print(profile)
        df, dfwko = ramp_test_activity(profile, ftp=ftp)
        wko1 = make_zwo_from_ramp(dfwko, filename=None, name=f"{name}_ftp_{ftp}", ftp=ftp)
        wko2 = make_zwo_from_ramp(dfwko, filename=None, name=f"{name}_ftp_1", ftp=1)
        wko_user = make_zwo_from_ramp(dfwko, filename=None, name=f"{name}_ftp_1", ftp=None)

        st.download_button(
            label="Full data as CSV",
            data=df[[c for c in df.columns if "power_seconds" not in c]].to_csv(index=False).encode("utf-8"),
            file_name=f"ramp_test_{name}.csv",
            mime="text/csv",
        )
        st.download_button(
            label=f"Download WKO with ftp set to {ftp}",
            data=wko1.encode("utf-8"),
            file_name=f"ramp_test_{name}_ftp_{ftp}.zwo",
            mime="text/csv",
        )
        st.download_button(
            label="Download WKO with ftp set to 1",
            data=wko2.encode("utf-8"),
            file_name=f"ramp_test_{name}_ftp_1.zwo",
            mime="text/csv",
        )
        st.download_button(
            label="Download WKO with ftp set to in game ftp",
            data=wko_user.encode("utf-8"),
            file_name=f"ramp_test_{name}_ftp_user.zwo",
            mime="text/csv",
        )
