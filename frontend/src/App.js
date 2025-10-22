import React, { useState } from "react";

function App() {
  const [id, setId] = useState("");              // Store the input ID
  const [data, setData] = useState(null);        // Store fetched JSON object
  const [error, setError] = useState(null);      // Store error message
  const [loading, setLoading] = useState(false); // Loading state

  // Function to fetch data by ID
  const fetchByID = () => {
    if (!id) return; // Don't fetch if no ID entered

    setLoading(true);
    setError(null);
    setData(null);

    fetch(`http://localhost:5000/db/game?appid=${encodeURIComponent(id)}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Error: ${res.status} ${res.statusText}`);
        }
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

  return (
    <div>
      <h1>Search Thing by ID</h1>
      <input
        type="text"
        placeholder="Enter ID"
        value={id}
        onChange={(e) => setId(e.target.value)}
      />
      <button onClick={fetchByID} disabled={!id || loading}>
        {loading ? "Loading..." : "Fetch"}
      </button>

      <div style={{ marginTop: "1rem" }}>
        {error && <p style={{ color: "red" }}>Error: {error}</p>}

        {data && (
          <pre
            style={{
              backgroundColor: "#f0f0f0",
              padding: "1rem",
              borderRadius: "4px",
              whiteSpace: "pre-wrap",
            }}
          >
            {JSON.stringify(data, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}

export default App;
