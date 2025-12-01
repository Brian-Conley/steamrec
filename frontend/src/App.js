import React, { useState } from "react";

function App() {
  const [id, setId] = useState("");
  const [tags, setTags] = useState("");
  const [price, setPrice] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [steamId, setSteamId] = useState("");
  const [maxPlayers, setMaxPlayers] = useState("");
  const [minReviews, setMinReviews] = useState("");

  // Helper fetch wrapper
  const doFetch = (url, options = {}) => {
    setLoading(true);
    setError(null);
    setData(null);

    fetch(url, options)
      .then((res) => {
        if (!res.ok) throw new Error(`Error: ${res.status} ${res.statusText}`);
        return res.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  const fetchByID = () => {
    if (!id) return;
    doFetch(`http://localhost:5000/db/game?appid=${encodeURIComponent(id)}`);
  };

  const fetchByLibrary = async () => {
    if (!steamId) return;

    setLoading(true);
    setError(null);
    setData(null);

    try {
      // Sync user library
      const syncRes = await fetch(`http://localhost:5000/sync_user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ steamid: steamId }),
      });

      if (!syncRes.ok) {
        const errText = await syncRes.text();
        throw new Error(`Sync failed: ${errText}`);
      }

      const syncJson = await syncRes.json();

      // Show the result of syncing (game count)
      setData(syncJson);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendations = async () => {
  if (!steamId) return;

  setLoading(true);
  setError(null);
  setData(null);

  try {
    const recRes = await fetch(
      `http://localhost:5000/recommend?steamid=${encodeURIComponent(steamId)}`
    );

    if (!recRes.ok) {
      const errText = await recRes.text();
      throw new Error(`Recommendation failed: ${errText}`);
    }

    const recJson = await recRes.json();
    setData(recJson); // will trigger your recommendation cards
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

  const insertGame = () => {
    doFetch(`http://localhost:5000/db/insert?appid=${encodeURIComponent(id)}`, {
      method: "POST",
    });
  };

  const updateGame = () => {
    doFetch(
      `http://localhost:5000/db/update?appid=${encodeURIComponent(
        id
      )}&price=${encodeURIComponent(price)}`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ appid: id, price }),
      }
    );
  };

  const deleteGame = () => {
    doFetch(
      `http://localhost:5000/db/delete?appid=${encodeURIComponent(id)}`,
      { method: "DELETE" }
    );
  };

  const fetchByTags = () => {
    if (!tags) return;
    doFetch(
      `http://localhost:5000/db/searchByTags?tags=${encodeURIComponent(tags)}`
    );
  };

  const fetchUnpopular = () => {
    const qs = new URLSearchParams();
    if (maxPlayers) qs.append("max_players", maxPlayers);
    if (minReviews) qs.append("min_reviews", minReviews);

    doFetch(`http://localhost:5000/db/unpopular?${qs.toString()}`);
  };

  // ---------------------
  // RENDER: Recommendation cards
  // ---------------------
  const renderRecommendations = (list) => {
    if (!Array.isArray(list)) return null;

    return (
      <div className="recommendations">
        <h3>Recommended Games</h3>
          <div className="cards">
            {list.map((game) => (
              <div key={game.appid} className="card">
                <h4>{game.name || "Unknown Title"}</h4>

              <p><strong>App ID:</strong> {game.appid}</p>

              {game.price !== undefined && (
                <p><strong>Price:</strong> ${game.price}</p>
              )}

              {game.tags && (
                <p><strong>Tags:</strong> {game.tags.join(", ")}</p>
              )}

              <a
                href={`https://store.steampowered.com/app/${game.appid}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                View on Steam →
              </a>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div>
      <h2>Steam Game Recommendations</h2>

      <input
        type="text"
        placeholder="Enter App ID"
        value={id}
        onChange={(e) => setId(e.target.value)}
      />
      <input
        type="number"
        placeholder="Enter Price"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
      />
      <input
        type="text"
        placeholder="Search by tags (e.g. action,rpg)"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
      />
      <input
        type="text"
        placeholder="Enter SteamID to fetch recommendations"
        value={steamId}
        onChange={(e) => setSteamId(e.target.value)}
      />
      <input
        type="number"
        placeholder="Max player count (e.g. < 100)"
        value={maxPlayers}
        onChange={(e) => setMaxPlayers(e.target.value)}
      />
      <input
        type="number"
        placeholder="Min reviews"
        value={minReviews}
        onChange={(e) => setMinReviews(e.target.value)}
      />

      <div>
        <button onClick={fetchByID}>Fetch</button>
        <button onClick={fetchByTags}>Search by Tags</button>
        <button onClick={fetchByLibrary}>Search by SteamID</button>
        <button onClick={fetchRecommendations}>Recommend Based on Library</button>
        <button onClick={fetchUnpopular}>Search for Hidden Gems</button>
        <button onClick={insertGame}>Insert</button>
        <button onClick={updateGame}>Update</button>
        <button onClick={deleteGame}>Delete</button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {/* JSON fallback */}
      {data && !Array.isArray(data) && (
        <pre>
          {JSON.stringify(data, null, 2)}
        </pre>
      )}

      {/* Show owned library list */}
      {data && data.owned_games && !Array.isArray(data) && (
        <div className="library">
          <h3>Owned Games ({data.total_games})</h3>
          <ul>
            {data.owned_games.map(g => (
              <li key={g.appid}>
                {g.name} (AppID: {g.appid})
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendation cards */}
      {Array.isArray(data) && renderRecommendations(data)}
    </div>
  );
}

export default App;
