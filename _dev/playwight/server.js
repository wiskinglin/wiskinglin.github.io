import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { extractData } from './extractor.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('public'));

// API Endpoint for extraction
app.post('/api/extract', async (req, res) => {
  const { url } = req.body;
  if (!url) {
    return res.status(400).json({ error: 'URL is required' });
  }

  try {
    const data = await extractData(url);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`\n[🚀] Server running at http://localhost:${PORT}`);
  console.log(`[🌐] Open your browser to access the extractor interface.\n`);
});
