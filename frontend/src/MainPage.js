import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function MainPage() {
  const navigate = useNavigate();

  const [id, setId] = useState("");
  const [price, setPrice] = useState("");
  const [steamId, setSteamId] = useState("");

  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

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
      const syncRes = await fetch(`http://localhost:5000/sync_user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ steamid: steamId }),
      });

      if (!syncRes.ok) {
        const errText = await syncRes.text();
        throw new Error(`Sync failed: ${errText}`);
      }

      const json = await syncRes.json();
      setData(json);
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

      const json = await recRes.json();
      setData(json);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchUnpopular = () => {
  if (!steamId) {
    setError("Please enter a SteamID first.");
    return;
  }

  doFetch(
    `http://localhost:5000/recommend/hidden-gems?steamid=${encodeURIComponent(
      steamId
    )}`
  );
};


  const insertGame = () => {
    doFetch(
      `http://localhost:5000/db/insert?appid=${encodeURIComponent(id)}`,
      { method: "POST" }
    );
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
                <p><strong>Price:</strong> ${(game.price / 100).toFixed(2)}</p>
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
      <button
        style={{
          marginBottom: "20px",
          padding: "10px 15px",
          fontSize: "16px",
          fontWeight: "bold",
        }}
        onClick={() => navigate("/search")}
      >
        🔎 Go to Search Page
      </button>

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
        placeholder="Enter SteamID to fetch recommendations"
        value={steamId}
        onChange={(e) => setSteamId(e.target.value)}
      />

      <div>
        <button onClick={fetchByID}>Fetch</button>
        <button onClick={fetchByLibrary}>Sync Library</button>
        <button onClick={fetchRecommendations}>Recommend Based on Library</button>
        <button onClick={fetchUnpopular}>Hidden Gems</button>
        <button onClick={insertGame}>Insert</button>
        <button onClick={updateGame}>Update</button>
        <button onClick={deleteGame}>Delete</button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {data && !Array.isArray(data) && !data.owned_games && (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      )}

      {data && data.owned_games && (
        <div className="library">
          <h3>Owned Games ({data.total_games})</h3>
          <ul>
            {data.owned_games.map((g) => (
              <li key={g.appid}>
                {g.name} (AppID: {g.appid})
              </li>
            ))}
          </ul>
        </div>
      )}

      {Array.isArray(data) && renderRecommendations(data)}
    </div>
  );
}

export default MainPage;
