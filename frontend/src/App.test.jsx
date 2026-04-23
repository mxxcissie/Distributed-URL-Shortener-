import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App";

describe("App", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("shortens a URL and pre-fills the stats code", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        short_url: "http://127.0.0.1:8000/abc123",
      }),
    });

    render(<App />);

    await userEvent.type(
      screen.getByPlaceholderText("Enter a long URL (https://example.com)"),
      "https://example.com",
    );
    await userEvent.click(screen.getByRole("button", { name: "Shorten URL" }));

    expect(
      await screen.findByRole("link", { name: "http://127.0.0.1:8000/abc123" }),
    ).toBeInTheDocument();
    expect(screen.getByDisplayValue("abc123")).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:8000/shorten", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        original_url: "https://example.com",
      }),
    });
  });

  it("shows the click count for a short code", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        click_count: 7,
      }),
    });

    render(<App />);

    await userEvent.type(
      screen.getByPlaceholderText("Enter short code"),
      "abc123",
    );
    await userEvent.click(screen.getByRole("button", { name: "Get Stats" }));

    expect(await screen.findByText("7")).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:8000/stats/abc123");
  });

  it("surfaces backend error details", async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({
        detail: "Rate limit exceeded. Try again later.",
      }),
    });

    render(<App />);

    await userEvent.type(
      screen.getByPlaceholderText("Enter a long URL (https://example.com)"),
      "https://example.com",
    );
    await userEvent.click(screen.getByRole("button", { name: "Shorten URL" }));

    expect(
      await screen.findByText("Rate limit exceeded. Try again later."),
    ).toBeInTheDocument();
  });

  it("falls back to a generic message when the backend response is not JSON", async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => {
        throw new Error("Invalid JSON");
      },
    });

    render(<App />);

    await userEvent.type(
      screen.getByPlaceholderText("Enter short code"),
      "missing",
    );
    await userEvent.click(screen.getByRole("button", { name: "Get Stats" }));

    await waitFor(() => {
      expect(screen.getByText("Failed to fetch stats.")).toBeInTheDocument();
    });
  });
});
