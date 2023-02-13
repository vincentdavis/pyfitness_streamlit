import streamlit as st
import s3fs
def get_space():
    spaces = st.secrets['spaces']
    fs = s3fs.S3FileSystem(key=spaces['KEY'],
                           secret=spaces['SECRET'],
                           use_ssl=True,
                           anon=False,
                           client_kwargs={'endpoint_url': "https://nyc3.digitaloceanspaces.com"})
    return fs