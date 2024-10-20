const express = require('express');
const { Pool } = require('pg');
const bodyParser = require('body-parser')
const path = require('path');

const app = express();

app.use(express.static(path.join(__dirname, 'public')));
app.set("view engine", "ejs")
app.use(bodyParser.urlencoded({extended: true}))

function calculateHealthScore(weight, exerciseCount, totalExerciseDuration, calories) {
  let score = 0;

  const idealWeight = 22 * (1.8 * 1.8); // Example: ideal weight for 180cm height
  const weightDiff = Math.abs(weight - idealWeight);
  if (weightDiff <= 5) score += 1;
  else if (weightDiff <= 10) score += 0.5;

  if (exerciseCount > 0) {
    score += 0.5;
    if (totalExerciseDuration >= 30) score += 0.5;
    if (totalExerciseDuration >= 60) score += 0.5;
  }

  if (calories >= 1800 && calories <= 2200) score += 1;
  else if (calories >= 1600 && calories <= 2400) score += 0.5;
  return Math.min(4, score); // Ensure the score doesn't exceed 4
}

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

app.get("/stats"), (req, res) => {
  res.render("stats.ejs")
}

app.post("/setweight", async (req, res) => {
  const weight = req.body.weight;
  const exerciseCount = req.body.exerciseCount;
  const calories = req.body.calories;

  try {
    // Start a transaction
    await pool.query('BEGIN');

    // Insert user stats
    const userStatResult = await pool.query(
        'INSERT INTO exercises (calories_burned) VALUES ($1, $2) RETURNING id',
        [calories]
    );
    const userStatId = userStatResult.rows[0].id;

    console.log(`Weight: ${weight}`);
    console.log(`Number of exercises: ${exerciseCount}`);
    console.log(`Calories: ${calories}`);

    let totalExerciseDuration = 0;
    for (let i = 0; i < exerciseCount; i++) {
      const exerciseType = req.body[`exerciseType${i}`];
      const exerciseDuration = req.body[`exerciseDuration${i}`];
      await pool.query(
          'INSERT INTO exercises (user_stat_id, exercise_type, duration) VALUES ($1, $2, $3)',
          [userStatId, exerciseType, exerciseDuration]
      );
      totalExerciseDuration += exerciseDuration;
      console.log(`Exercise ${i + 1}: ${exerciseType} for ${exerciseDuration} minutes`);
    }
    const healthScore = calculateHealthScore(weight, exerciseCount, totalExerciseDuration, calories);
    await pool.query('INSERT INTO users (sentiment) VALUES ($1)', healthScore)

    await pool.query('COMMIT');
    res.redirect('/stats');
  } catch (err) {
    await pool.query('ROLLBACK');
    console.error(err);
    res.status(500).send("An error occurred while saving the data");
  }

  // Here you would typically save this data to your database

  res.redirect('/'); // change to redirect to stats page
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