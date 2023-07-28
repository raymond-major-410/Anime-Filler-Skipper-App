import streamlit as st
import anime_processor,gogoanime_api

st.title("Anime Filler Skip Application")
st.write("Select an anime from the list below and we will return all of the canon episodes")

#get anime drop down menu
anime_list = anime_processor.get_anime_list()
anime_show_names = []
for anime in anime_list:
    anime_show_names.append(anime['show_name'])

anime_selection = st.selectbox('Select an anime', anime_show_names)
st.write("You selected: ", anime_selection)

#get canon eps list of selected anime
if anime_selection is not None: 
    anime_ref_name = []
    for anime in anime_list:
        if anime['show_name'] == anime_selection:
              anime_ref_name.append(anime['link'])

    canon_eps = anime_processor.get_nonfiller_eps(anime_ref_name[0])

    st.subheader("Canon Episodes List")
    ep_selection = st.selectbox("Select an episode: ",canon_eps)

#get streaming link for selected episode
if ep_selection is not None:
    st.subheader("Watch Episode")
    anime_search_val = anime_processor.remove_non_numeric_parentheses(anime_selection)
    anime_id = gogoanime_api.get_anime_id(anime_search_val)
    if anime_id is not None:
        ep_link = gogoanime_api.get_ep_link(anime_id,ep_selection)
        if ep_link is not None:
            st.write("Stream Link: ", ep_link[0]['link'])
            #st.video(ep_link[0]['link']) - unable to get proper mime type from api



