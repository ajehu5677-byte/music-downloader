<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MP3 Juice - Stream & Download Global Music</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Circular', Arial, sans-serif; }
        
        body { background-color: #121212; color: #ffffff; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding-bottom: 60px; overflow-x: hidden; }
        header { width: 100%; display: flex; justify-content: center; gap: 30px; padding: 25px 0; font-size: 14px; background-color: #000000; margin-bottom: 20px; }
        header a { color: #b3b3b3; text-decoration: none; font-weight: bold; }
        header a:hover { color: #ffffff; }
        
        #content { width: 100%; max-width: 680px; padding: 0 20px; text-align: center; }
        .brand-title { font-size: 42px; font-weight: 900; letter-spacing: -1px; margin-bottom: 25px; color: #1DB954; }
        
        .search-box-form { width: 100%; margin-bottom: 25px; }
        .search-box-container { display: flex; background-color: #242424; border-radius: 50px; overflow: hidden; border: 1px solid transparent; transition: border 0.2s ease; }
        .search-box-container:focus-within { border: 1px solid #ffffff; }
        .search-box-container input { flex: 1; border: none; background: none; padding: 16px 24px; font-size: 16px; outline: none; color: #ffffff; }
        .search-box-container input::placeholder { color: #757575; }
        .search-box-container button { background: none; border: none; padding: 0 24px; cursor: pointer; font-size: 18px; color: #b3b3b3; }
        .search-box-container button:hover { color: #ffffff; }
        
        #resultsContainer { width: 100%; display: flex; flex-direction: column; gap: 12px; margin-bottom: 30px; }
        .track-row-card { display: flex; align-items: center; justify-content: space-between; background-color: #181818; border-radius: 8px; padding: 14px 20px; transition: background-color 0.2s ease; border: 1px solid #282828; }
        .track-row-card:hover { background-color: #282828; }
        
        .track-info-block { text-align: left; flex: 1; padding-right: 15px; }
        .track-row-title { font-size: 16px; font-weight: bold; color: #ffffff; margin-bottom: 4px; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .track-row-artist { font-size: 14px; color: #b3b3b3; display: block; }
        
        .track-actions { display: flex; gap: 10px; align-items: center; }
        .card-btn { background-color: #1DB954; color: #ffffff; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 50px; cursor: pointer; transition: transform 0.1s ease; }
        .card-btn:hover { transform: scale(1.04); background-color: #1ed760; }
        .card-btn.play-btn { background-color: #ffffff; color: #000000; }
        .card-btn.play-btn:hover { background-color: #f6f6f6; }
        
        .server-download-container { display: none; width: 100%; background-color: #181818; border-radius: 12px; padding: 30px; border: 1px solid #282828; margin-top: 10px; }
        .player-wrapper { width: 100%; margin: 20px 0; background: #242424; padding: 15px; border-radius: 8px; }
        audio { width: 100%; outline: none; }
        
        .bitrate-link-row { display: inline-block; background-color: #1DB954; color: #ffffff; text-decoration: none; padding: 14px 32px; border-radius: 50px; font-size: 15px; font-weight: bold; margin-top: 15px; transition: transform 0.1s ease; }
        .bitrate-link-row:hover { transform: scale(1.04); background-color: #1ed760; }

        /* Modernized Looping Left Sidebar Sharing Deck Setup Styles */
        .sharing-sidebar { position: fixed; left: 0; top: 35%; display: flex; flex-direction: column; width: 45px; z-index: 9999; box-shadow: 2px 0 10px rgba(0,0,0,0.5); border-top-right-radius: 6px; border-bottom-right-radius: 6px; overflow: hidden; }
        .share-btn { width: 45px; height: 45px; display: none; align-items: center; justify-content: center; color: #ffffff; text-decoration: none; font-size: 18px; font-weight: bold; transition: all 0.3s ease; transform: translateX(-45px); opacity: 0; }
        
        /* Show Active Keyframe Animation Slide Block Layout */
        .share-btn.slide-active { display: flex; transform: translateX(0); opacity: 1; }
        
        .share-fb { background-color: #1877F2; }
        .share-msg { background-color: #0084FF; }
        .share-ig { background-color: #E1306C; }
        .share-tk { background-color: #000000; border-right: 1px solid #282828; }
    </style>
</head>
<body>
    <!-- Automated Looping Sharing Sidebar Buttons Element Container Deck -->
    <div class="sharing-sidebar" id="shareSidebar">
        <a href="javascript:void(0)" onclick="shareLink('fb')" class="share-btn share-fb slide-active">👤</a>
        <a href="javascript:void(0)" onclick="shareLink('msg')" class="share-btn share-msg">💬</a>
        <a href="javascript:void(0)" onclick="shareLink('ig')" class="share-btn share-ig">📸</a>
        <a href="javascript:void(0)" onclick="shareLink('tk')" class="share-btn share-tk">🎵</a>
    </div>

    <header><a href="#">Home</a><a href="#">FAQ</a><a href="#">DMCA</a><a href="#">Contact</a></header>
    <div id="content">
        <div class="brand-container"><div class="brand-title">Mp3Juice</div></div>
        <form class="search-box-form" id="searchForm" onsubmit="event.preventDefault(); performSearch();">
            <div class="search-box-container">
                <input type="text" id="queryInput" placeholder="What do you want to listen to?">
                <button type="submit" id="searchBtn">🔍</button>
            </div>
        </form>
        
        <div id="resultsContainer"></div>
        
        <div id="serverDownloadPanel" class="server-download-container">
            <h3 id="serverTitle" style="font-size: 20px; margin-bottom: 5px;">Track Name</h3>
            <p id="serverArtist" style="color: #b3b3b3; font-size: 14px; margin-bottom: 15px;">Artist Name</p>
            
            <div class="player-wrapper">
                <p style="font-size: 12px; color: #b3b3b3; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; font-weight: bold;">🎵 Live Preview Player</p>
                <audio id="audioStreamPlayer" controls src=""></audio>
            </div>
            
            <a href="#" id="finalDownloadBtn" class="bitrate-link-row">📥 Download MP3 Audio File</a>
            <div style="margin-top: 20px;"><a href="javascript:location.reload()" style="color:#b3b3b3; font-size:13px; text-decoration:none; font-weight:bold;">← Search Another Song</a></div>
        </div>
    </div>
    
    <script>
        // Looping Left Sidebar 3-Second Automatic Sliding Animation Sequencer Script
        let currentShareIndex = 0;
        const shareButtons = document.querySelectorAll('.share-btn');
        
        setInterval(() => {
            // Hide the active item out of view smoothly
            shareButtons[currentShareIndex].classList.remove('slide-active');
            
            // Increment rotation array indexes cleanly
            currentShareIndex = (currentShareIndex + 1) % shareButtons.length;
            
            // Pop the next social handle network icon item straight into active layout view
            shareButtons[currentShareIndex].classList.add('slide-active');
        }, 3000);

        function shareLink(platform) {
            const currentUrl = encodeURIComponent(window.location.href);
            const alertText = "Share link copied! Post it to your profile screen layout context.";
            
            navigator.clipboard.writeText(window.location.href);
            
            if (platform === 'fb') window.open(`https://facebook.com{currentUrl}`, '_blank');
            if (platform === 'msg') window.open(`fb-messenger://share?link=${currentUrl}`, '_blank');
            if (platform === 'ig') alert("Instagram doesn't support direct web sharing links. " + alertText);
            if (platform === 'tk') alert("TikTok link sharing ready. " + alertText);
        }

        function performSearch() {
            const queryVal = document.getElementById('queryInput').value.trim();
            if (!queryVal) return alert("Please type a track name first.");
            document.getElementById('searchBtn').innerText = "⏳";
            
            fetch(`https://saavn.dev{encodeURIComponent(queryVal)}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('searchBtn').innerText = "🔍";
                const container = document.getElementById('resultsContainer');
                container.innerHTML = "";
                document.getElementById('serverDownloadPanel').style.display = 'none';
                
                const items = data.data?.results || [];
                if (items.length > 0) {
                    items.slice(0, 5).forEach(track => {
                        const card = document.createElement('div');
                        card.className = 'track-row-card';
                        
                        // FIXED: Completely clean artist extraction to fix the network lag popup crash bug 
                        const trackName = track.name || 'Unknown Track';
                        let artistName = 'Various Artists';
                        
                        if (track.artists && track.artists.primary && track.artists.primary.length > 0) {
                            artistName = track.artists.primary[0].name || 'Various Artists';
                        } else if (track.artists && track.artists.all && track.artists.all.length > 0) {
                            artistName = track.artists.all[0].name || 'Various Artists';
                        }
                        
                        const cleanTitle = `${artistName} - ${trackName}`.replace(/'/g, "\\'");
                        
                        // Safely retrieve high-quality streaming addresses directly from data response arrays
                        let streamUrl = '';
                        if (track.downloadUrl && track.downloadUrl.length > 0) {
                            streamUrl = track.downloadUrl[track.downloadUrl.length - 1].url || '';
                        }
                        
                        card.innerHTML = `
                            <div class="track-info-block">
                                <span class="track-row-title">${trackName}</span>
                                <span class="track-row-artist">${artistName}</span>
                            </div>
                            <div class="track-actions">
                                <button class="card-btn play-btn" onclick="openMediaControlPanel('${cleanTitle}', '${artistName}', '${streamUrl}', true)">Play</button>
                                <button class="card-btn" onclick="openMediaControlPanel('${cleanTitle}', '${artistName}', '${streamUrl}', false)">Download</button>
                            </div>
                        `;
                        container.appendChild(card);
                    });
                } else {
                    alert("No matching song titles found globally. Try another term phrase.");
                }
            })
            .catch(err => {
                document.getElementById('searchBtn').innerText = "🔍";
                alert("Search connection reset. Type your keywords and click search again.");
                console.error(err);
            });
        }

        function openMediaControlPanel(fullTitle, artist, streamUrl, autoPlayActive) {
            document.getElementById('resultsContainer').innerHTML = "";
            document.getElementById('serverTitle').innerText = fullTitle;
            document.getElementById('serverArtist').innerText = artist;
            
            const playerElement = document.getElementById('audioStreamPlayer');
            playerElement.src = streamUrl;
            playerElement.load();
            
            if(autoPlayActive && streamUrl) {
                playerElement.play().catch(e => console.log("User interaction requirement check"));
            }
            
            const targetQueryUrl = `ytsearch:${fullTitle} official audio`;
            const downloadUrl = `/download_proxy?url=${encodeURIComponent(targetQueryUrl)}&title=${encodeURIComponent(fullTitle)}`;
            document.getElementById('finalDownloadBtn').href = downloadUrl;
            
            document.getElementById('serverDownloadPanel').style.display = 'block';
        }
    </script>
</body>
</html>
