const express = require('express');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

const pool = new Pool({
//  user: 'your_username',
  host: 'localhost',
  database: 'uncdb',
//  password: 'your_password',
  port: 5432,
});

app.get('/debug_all_users', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM users');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
app.post('/setweight', (req, res) => {
  const number = req.body.number;

  if (typeof number === 'number' && Number.isInteger(number)) {
    console.log(`Received integer: ${number}`);
    res.status(200).json({ message: `Received and printed integer: ${number}` });
  } else {
    res.status(400).json({ error: 'Invalid input. Please provide an integer.' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/stat-form.html');
});