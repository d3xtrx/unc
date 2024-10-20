const express = require('express');
const { Pool } = require('pg');
const bodyParser = require('body-parser')
const path = require('path');

const app = express();

app.use(express.static(path.join(__dirname, 'public')));
app.set("view engine", "ejs")
app.use(bodyParser.urlencoded({extended: true}))


app.get("/", (req, res)=> {
  res.render("index.ejs")
})

app.get("/index", (req, res)=> {
  res.render("index.ejs")
})

app.get("/stat-form", (req, res)=> {
  res.render("stat-form.ejs")
})

app.get("/unc-store", (req, res)=> {
  res.render("unc-store.ejs")
})

app.post("/setweight", (req, res) => {
  const weight = req.body.weight;
  const exerciseCount = req.body.exerciseCount;
  const calories = req.body.calories;

  console.log(`Weight: ${weight}`);
  console.log(`Number of exercises: ${exerciseCount}`);
  console.log(`Calories: ${calories}`);

  // Process exercise data
  for (let i = 0; i < exerciseCount; i++) {
    const exerciseType = req.body[`exerciseType${i}`];
    const exerciseDuration = req.body[`exerciseDuration${i}`];
    console.log(`Exercise ${i + 1}: ${exerciseType} for ${exerciseDuration} minutes`);
  }

  // Here you would typically save this data to your database

  res.redirect('/'); // Redirect to home page or a confirmation page
});

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

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));