def get_current_song(artist, track, authentication):
    # search in spotify
    results = authentication.search(q=f"artist:{artist} track:{track}")

    # extract URL from results
    entire_song = results["tracks"]["items"][0]["external_urls"]["spotify"]

    return entire_song