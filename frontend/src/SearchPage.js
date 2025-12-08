import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function SearchPage() {

  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [developer, setDeveloper] = useState("");
  const [publisher, setPublisher] = useState("");
  const [category, setCategory] = useState("");
  const [tags, setTags] = useState("");
  const [priceMin, setPriceMin] = useState("");
  const [priceMax, setPriceMax] = useState("");

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const doFetch = (url) => {
    setLoading(true);
    setError(null);
    setData(null);

    fetch(url)
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

  const search = () => {
    const qs = new URLSearchParams();

    if (name) qs.append("name", name);
    if (developer) qs.append("developer", developer);
    if (publisher) qs.append("publisher", publisher);
    if (category) qs.append("category", category);
    if (tags) qs.append("tags", tags);
    if (priceMin) qs.append("price_min", priceMin);
    if (priceMax) qs.append("price_max", priceMax);

    const url = `http://localhost:5000/db/search?${qs.toString()}`;
    doFetch(url);
  };

  // Reusing your card layout
  const renderCards = (games) => {
    return (
      <div className="recommendations">
        <h3>Search Results</h3>

        <div className="cards">
          {games.map((g) => (
            <div key={g.appid} className="card">
              <h4>{g.name}</h4>
              <p><strong>App ID:</strong> {g.appid}</p>

              {g.price !== undefined && (
                <p><strong>Price:</strong> ${(g.price / 100).toFixed(2)}</p>
              )}

              {g.tags && (
                <p><strong>Tags:</strong> {g.tags.join(", ")}</p>
              )}

              <a
                href={`https://store.steampowered.com/app/${g.appid}`}
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
          onClick={() => navigate("/")}
        >
          ← Back to Home
      </button>

      <h2>Advanced Game Search</h2>

      {/* Same styling as App.js */}
      <input
        type="text"
        placeholder="Search by name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <input
        type="text"
        placeholder="Developer"
        value={developer}
        onChange={(e) => setDeveloper(e.target.value)}
      />

      <input
        type="text"
        placeholder="Publisher"
        value={publisher}
        onChange={(e) => setPublisher(e.target.value)}
      />

      <input
        type="text"
        placeholder="Category (comma separated)"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      />

      <input
        type="text"
        placeholder="Tags (comma separated)"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
      />

      <input
        type="number"
        placeholder="Min Price"
        value={priceMin}
        onChange={(e) => setPriceMin(e.target.value)}
      />

      <input
        type="number"
        placeholder="Max Price"
        value={priceMax}
        onChange={(e) => setPriceMax(e.target.value)}
      />

      <div>
        <button onClick={search}>Search</button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {/* Show results */}
      {Array.isArray(data) && renderCards(data)}
    </div>
  );
}

export default SearchPage;
