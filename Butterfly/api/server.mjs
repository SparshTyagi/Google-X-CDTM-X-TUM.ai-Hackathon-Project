import express from "express";
import { Storage } from "@google-cloud/storage";

const port = process.env.PORT || 8080;
const BUCKET = process.env.BUCKET || "trendscouter-data-tum-cdtm25mun-8792";
const FILE = process.env.FILE || "trends/latest.json";

const storage = new Storage();
const app = express();

app.get(['/trends', '/api/trends'], async (_req, res) => {
  try {
    const [buf] = await storage.bucket(BUCKET).file(FILE).download();
    res.set("Content-Type", "application/json");
    res.set("Cache-Control", "public, max-age=30");
    res.send(buf.toString("utf-8"));
  } catch (e) {
    console.error("Error fetching GCS file:", e);
    res.status(500).json({ error: "Failed to load trends data" });
  }
});

// optional: health route for both
app.get(['/healthz', '/api/healthz'], (_req, res) => res.send('ok'));

app.listen(port, () => console.log("API listening on", port));
