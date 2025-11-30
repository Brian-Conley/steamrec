import React, { useState } from "react";

function App() {
  const [id, setId] = useState("");
  const [tags, setTags] = useState("");
  const [price, setPrice] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [steamId, setSteamId] = useState("");

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

  const fetchByLibrary = () => {
    if (!steamId) return;
    doFetch(`http://localhost:5000/steam/library?steamid=${encodeURIComponent(steamId)}`);
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

  // ---------------------
  // RENDER: Recommendation cards
  // ---------------------
  const renderRecommendations = (list) => {
    if (!Array.isArray(list)) return null;

    return (
      <div style={{ marginTop: "1rem" }}>
        <h3>Recommended Games</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
          {list.map((game) => (
            <div
              key={game.appid}
              style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "1rem",
                width: "260px",
                background: "#fafafa",
              }}
            >
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
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
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

      <div style={{ marginTop: "1rem" }}>
        <button onClick={fetchByID}>Fetch</button>
        <button onClick={fetchByTags}>Search by Tags</button>
        <button onClick={fetchByLibrary}>Search by SteamID</button>
        <button onClick={insertGame}>Insert</button>
        <button onClick={updateGame}>Update</button>
        <button onClick={deleteGame}>Delete</button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {/* JSON fallback */}
      {data && !Array.isArray(data) && (
        <pre style={{ backgroundColor: "#f0f0f0", padding: "1rem" }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      )}

      {/* Recommendation cards */}
      {Array.isArray(data) && renderRecommendations(data)}
    </div>
  );
}

export default App;
