import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="64-Bit Music Player",
    page_icon="🎵",
    layout="wide"
)

# ---------------- CSS (SPOTIFY-STYLE) ----------------
st.markdown("""
<style>
/* Base Styles */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #121212 !important;
    color: white !important;
}

.block-container {
    padding-bottom: 140px !important;
    padding-top: 3rem !important;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Header */
.app-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: linear-gradient(180deg, #000 0%, #121212 100%);
    padding: 1.5rem;
    font-size: 2rem;
    font-weight: 700;
    border-bottom: 1px solid #282828;
    text-align: center;
    margin-bottom: 2rem;
}

/* Search Input */
.stTextInput > div > div > input {
    background: #1f1f1f !important;
    color: white !important;
    border-radius: 25px !important;
    border: 1px solid #333 !important;
    padding: 0.8rem 1.5rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #1db954 !important;
    box-shadow: 0 0 15px rgba(29, 185, 84, 0.3) !important;
}

/* Search Button */
.stButton > button {
    background: #1db954 !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: #1ed760 !important;
    transform: scale(1.05) !important;
}

/* Song Card */
.song-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.8rem;
    border-radius: 8px;
    background: #181818;
    margin-bottom: 0.6rem;
    transition: background 0.2s ease;
    border: 1px solid transparent;
}

.song-card:hover {
    background: #282828;
    border-color: #333;
    cursor: pointer;
}

.song-card img {
    width: 55px;
    height: 55px;
    border-radius: 6px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}

.song-info {
    flex: 1;
}

.song-title {
    font-weight: 600;
    font-size: 1rem;
    color: white;
    margin-bottom: 0.3rem;
}

.song-artist {
    font-size: 0.85rem;
    color: #b3b3b3;
}

/* Section Header */
h1, h2, h3 {
    color: white !important;
}

.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 2rem 0 1rem 0;
    color: white;
}

/* Bottom Player */
.player {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: linear-gradient(180deg, #181818 0%, #000 100%);
    border-top: 1px solid #282828;
    padding: 1rem;
    z-index: 200;
    box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.5);
}

.player-inner {
    display: flex;
    align-items: center;
    gap: 1rem;
    max-width: 1200px;
    margin: 0 auto;
}

.player img {
    width: 60px;
    height: 60px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}

.player-info {
    flex: 1;
}

.player-title {
    font-weight: 600;
    font-size: 0.95rem;
    color: white;
}

.player-artist {
    font-size: 0.8rem;
    color: #b3b3b3;
}

/* Audio Player */
audio {
    width: 100%;
    margin-top: 0.5rem;
    height: 40px;
}

audio::-webkit-media-controls-panel {
    background-color: #282828;
}

audio::-webkit-media-controls-play-button,
audio::-webkit-media-controls-pause-button {
    background-color: #1db954;
    border-radius: 50%;
}

/* Lyrics Expander */
.streamlit-expanderHeader {
    background: #282828 !important;
    border-radius: 8px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.8rem !important;
    border: 1px solid #333 !important;
}

.streamlit-expanderHeader:hover {
    background: #333 !important;
}

.streamlit-expanderContent {
    background: #181818 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    color: #b3b3b3 !important;
    max-height: 300px;
    overflow-y: auto;
    line-height: 1.8;
    margin-top: 0.5rem;
}

/* Spinner */
.stSpinner > div {
    border-color: #1db954 !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #181818;
}

::-webkit-scrollbar-thumb {
    background: #333;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}

/* Play Button in List */
[data-testid="column"]:last-child button {
    background: transparent !important;
    border: 2px solid #1db954 !important;
    color: #1db954 !important;
    border-radius: 50% !important;
    width: 45px !important;
    height: 45px !important;
    font-size: 1.2rem !important;
    padding: 0 !important;
    transition: all 0.3s ease !important;
}

[data-testid="column"]:last-child button:hover {
    background: #1db954 !important;
    color: white !important;
    transform: scale(1.1) !important;
}

/* Text Colors */
p, span, label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("results", [])
st.session_state.setdefault("current_song", None)
st.session_state.setdefault("lyrics", None)

# ---------------- HELPERS ----------------
def get_artists(song):
    if song.get("primaryArtists"):
        return song["primaryArtists"]
    primary = song.get("artists", {}).get("primary", [])
    if primary:
        return ", ".join(a.get("name", "") for a in primary)
    return "Unknown Artist"

def get_image(song):
    images = song.get("image", [])
    if images:
        return images[-1]["url"]
    return "https://via.placeholder.com/150"

def get_audio(song):
    for u in song.get("downloadUrl", []):
        if u.get("quality") == "320kbps":
            return u["url"]
    if song.get("downloadUrl"):
        return song["downloadUrl"][-1]["url"]
    return None

# ---------------- API ----------------
def search_songs(query):
    url = "https://saavn.sumit.co/api/search/songs"
    res = requests.get(url, params={"query": query}, timeout=10)
    data = res.json()
    if data.get("success"):
        return data["data"]["results"]
    return []

def fetch_lyrics(song_id):
    url = "https://saavn.sumit.co/api/lyrics"
    res = requests.get(url, params={"id": song_id}, timeout=10)
    data = res.json()
    if data.get("success"):
        return data["data"]["lyrics"]
    return None

# ---------------- HEADER ----------------
st.markdown("<div class='app-header'>🎧 64-Bit Music Player</div>", unsafe_allow_html=True)

# ---------------- SEARCH ----------------
query = st.text_input("🔍 Search songs, artists or albums", placeholder="Type song name...")

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    search_btn = st.button("Search", use_container_width=True)

if search_btn and query:
    with st.spinner("🎵 Searching..."):
        st.session_state.results = search_songs(query)
        if not st.session_state.results:
            st.warning("No songs found. Try a different search!")

# ---------------- SONG LIST ----------------
if st.session_state.results:
    st.markdown("<div class='section-header'>🎶 Search Results</div>", unsafe_allow_html=True)

    for song in st.session_state.results:
        col1, col2 = st.columns([8, 1])

        with col1:
            st.markdown(
                f"""
                <div class="song-card">
                    <img src="{get_image(song)}">
                    <div class="song-info">
                        <div class="song-title">{song.get("name", "Unknown Title")}</div>
                        <div class="song-artist">{get_artists(song)}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            if st.button("▶", key=song["id"], help="Play song"):
                st.session_state.current_song = song
                st.session_state.lyrics = fetch_lyrics(song["id"]) if song.get("hasLyrics") else None

# ---------------- BOTTOM PLAYER ----------------
if st.session_state.current_song:
    song = st.session_state.current_song
    audio_url = get_audio(song)

    st.markdown(
        f"""
        <div class="player">
            <div class="player-inner">
                <img src="{get_image(song)}">
                <div class="player-info">
                    <div class="player-title">{song.get("name", "Unknown")}</div>
                    <div class="player-artist">{get_artists(song)}</div>
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )

    if audio_url:
        st.audio(audio_url, format="audio/mp3")
    else:
        st.error("❌ Audio not available")

    if st.session_state.lyrics:
        with st.expander("📝 View Lyrics"):
            st.markdown(
                st.session_state.lyrics.replace("\n", "<br>"),
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)