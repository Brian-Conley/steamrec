import React, { useState } from "react";

function App() {
  const [id, setId] = useState("");              // Store the input ID
  const [name, setName] = useState("");          // New input for game name
  const [data, setData] = useState(null);        // Store fetched JSON object
  const [error, setError] = useState(null);      // Store error message
  const [loading, setLoading] = useState(false); // Loading state

  // Function to fetch data by ID
  const fetchByID = () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    setData(null);

    fetch(`http://localhost:5000/db/game?appid=${encodeURIComponent(id)}`)
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

  const insertGame = () => {
    fetch(`http://localhost:5000/db/game`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ appid: id, name }),
    })
      .then((res) => res.json())
      .then((json) => alert(json.status))
      .catch((err) => alert("Error: " + err.message));
  };

  return (
    <div>
      <h3>Game Database</h3>

      <input
        type="text"
        placeholder="Enter ID"
        value={id}
        onChange={(e) => setId(e.target.value)}
      />
      <input
        type="text"
        placeholder="Enter Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
      type="number"
      placeholder="Enter Price"
      value={price}
      onChange={(e) => setPrice(e.target.value)}
      />

      <div style={{ marginTop: "1rem" }}>
        <button onClick={fetchByID}>Fetch</button>
        <button onClick={insertGame}>Insert</button>

      </div>

      <div style={{ marginTop: "1rem" }}>
        {error && <p style={{ color: "red" }}>Error: {error}</p>}
        {data && (
          <pre style={{ backgroundColor: "#f0f0f0", padding: "1rem" }}>
            {JSON.stringify(data, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}

export default App;
