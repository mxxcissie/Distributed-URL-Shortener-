import React, { useState } from "react";
import "./App.css";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function getErrorMessage(response, fallbackMessage) {
  try {
    const data = await response.json();

    if (typeof data?.detail === "string" && data.detail.trim()) {
      return data.detail;
    }

    if (typeof data?.message === "string" && data.message.trim()) {
      return data.message;
    }
  } catch {
    return fallbackMessage;
  }

  return fallbackMessage;
}

export default function App() {
  const [originalUrl, setOriginalUrl] = useState("");
  const [shortenedUrl, setShortenedUrl] = useState("");
  const [statsCode, setStatsCode] = useState("");
  const [clickCount, setClickCount] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statsLoading, setStatsLoading] = useState(false);
  const [error, setError] = useState("");
  const [copyMessage, setCopyMessage] = useState("");

  const extractShortCode = (url) => {
    try {
      const parts = new URL(url).pathname.split("/").filter(Boolean);
      return parts[parts.length - 1] || "";
    } catch {
      return "";
    }
  };

  const handleShorten = async () => {
    setError("");
    setCopyMessage("");
    setShortenedUrl("");
    setClickCount(null);

    if (!originalUrl.trim()) {
      setError("Please enter a URL.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(`${API_BASE}/shorten`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          original_url: originalUrl,
        }),
      });

      if (!response.ok) {
        throw new Error(
          await getErrorMessage(response, "Failed to shorten URL."),
        );
      }

      const data = await response.json();

      const shortUrl =
        data.short_url || data.shortened_url || data.url || "";

      if (!shortUrl) {
        throw new Error("Short URL was not returned by the API.");
      }

      setShortenedUrl(shortUrl);
      setStatsCode(extractShortCode(shortUrl));
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const handleStats = async () => {
    setError("");
    setCopyMessage("");
    setClickCount(null);

    if (!statsCode.trim()) {
      setError("Please enter a short code.");
      return;
    }

    try {
      setStatsLoading(true);

      const response = await fetch(`${API_BASE}/stats/${statsCode}`);

      if (!response.ok) {
        throw new Error(
          await getErrorMessage(response, "Failed to fetch stats."),
        );
      }

      const data = await response.json();

      setClickCount(data.click_count ?? data.clicks ?? 0);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setStatsLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!shortenedUrl) return;

    try {
      await navigator.clipboard.writeText(shortenedUrl);
      setCopyMessage("Copied!");
      setTimeout(() => setCopyMessage(""), 1500);
    } catch {
      setCopyMessage("Copy failed.");
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h1>Distributed URL Shortener</h1>
        <p className="subtitle">
          Minimal React frontend for a distributed FastAPI backend using
          PostgreSQL and Redis.
        </p>

        <section className="section">
          <h2>Create Short URL</h2>
          <input
            className="input"
            type="text"
            placeholder="Enter a long URL (https://example.com)"
            value={originalUrl}
            onChange={(e) => setOriginalUrl(e.target.value)}
          />
          <button className="button" onClick={handleShorten} disabled={loading}>
            {loading ? "Shortening..." : "Shorten URL"}
          </button>
        </section>

        {shortenedUrl && (
          <section className="section result-box">
            <h2>Result</h2>
            <p>
              <strong>Original URL:</strong> {originalUrl}
            </p>
            <p>
              <strong>Short URL:</strong>{" "}
              <a href={shortenedUrl} target="_blank" rel="noreferrer">
                {shortenedUrl}
              </a>
            </p>
            <div className="button-row">
              <button className="button secondary" onClick={handleCopy}>
                Copy
              </button>
              {copyMessage && <span className="copy-message">{copyMessage}</span>}
            </div>
          </section>
        )}

        <section className="section">
          <h2>Check Stats</h2>
          <input
            className="input"
            type="text"
            placeholder="Enter short code"
            value={statsCode}
            onChange={(e) => setStatsCode(e.target.value)}
          />
          <button
            className="button"
            onClick={handleStats}
            disabled={statsLoading}
          >
            {statsLoading ? "Loading..." : "Get Stats"}
          </button>

          {clickCount !== null && (
            <div className="stats-box">
              <p>
                <strong>Click count:</strong> {clickCount}
              </p>
            </div>
          )}
        </section>

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
}
