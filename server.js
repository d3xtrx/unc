const express = require('express');
const { Pool } = require('pg');
const bodyParser = require('body-parser')
const path = require('path');
const cors = require('cors');

const app = express();

app.use(express.static(path.join(__dirname, 'public')));
app.set("view engine", "ejs")
app.use(bodyParser.urlencoded({extended: true}))
app.use(cors());

const pool = new Pool({
//  user: 'your_username',
  host: 'localhost',
  database: 'uncdb',
//  password: 'your_password',
  port: 5432,
});

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
  let minimized_score = Math.min(4, score); // Ensure the score doesn't exceed 4
  let intscore = parseInt(minimized_score, 10);
  return intscore;
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

app.get('/get_sentiment', async (req, res) => {
  console.log("GET /get_sentiment endpoint hit");
  try {
    const result = await pool.query('SELECT sentiment FROM users WHERE user_id = $1', [1]);
    console.log("Query result:", result.rows);
    if (result.rows.length > 0) {
      console.log("Sending sentiment:", result.rows[0].sentiment);
      res.json({ sentiment: result.rows[0].sentiment });
    } else {
      console.log("User not found");
      res.status(404).json({ error: 'User not found' });
    }
  } catch (err) {
    console.error("Error in /get_sentiment:", err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/get_avatar', async (req, res) => {
  console.log("GET /get_avatar endpoint hit");
  try {
    const result = await pool.query('SELECT avatar FROM users WHERE user_id = $1', [1]);
    console.log("Query result:", result.rows);
    if (result.rows.length > 0) {
      console.log("Sending sentiment:", result.rows[0].avatar);
      res.json({ avatar: result.rows[0].avatar});
    } else {
      console.log("User not found");
      res.status(404).json({ error: 'User not found' });
    }
  } catch (err) {
    console.error("Error in /get_sentiment:", err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get("/unc-store", (req, res)=> {
  res.render("unc-store.ejs")
})

app.get("/stats", (req, res) => {
  res.render("stats.ejs")
})

app.post("/set_avatar", async (req, res) => {
  const id = req.body.id;
  const name = req.body.name;

  await pool.query('BEGIN');
  await pool.query('UPDATE users SET avatar = $1 WHERE user_id IS NOT NULL', [id]);
  await pool.query('UPDATE users SET avatar_name = $1 WHERE user_id IS NOT NULL', [name]);
})
app.post("/setweight", async (req, res) => {
  const weight = req.body.weight;
  const exerciseCount = req.body.exerciseCount;
  const calories = req.body.calories;

  try {
    // Start a transaction
    await pool.query('BEGIN');

    // Insert user stats
    const userStatResult = await pool.query(
        'UPDATE users SET calories_burned = $1 WHERE user_id IS NOT NULL RETURNING user_id',
        [calories]
    );
    const userStatId = userStatResult.rows[0].user_id;

    console.log(`Weight: ${weight}`);
    console.log(`Number of exercises: ${exerciseCount}`);
    console.log(`Calories: ${calories}`);

    let totalExerciseDuration = 0;
    for (let i = 0; i < exerciseCount; i++) {
      const exerciseType = req.body[`exerciseType${i}`];
      const exerciseDuration = parseInt(req.body[`exerciseDuration${i}`], 10);
      await pool.query(
          'INSERT INTO exercises (user_id, exercise_type, duration) VALUES ($1, $2, $3)',
          [userStatId, exerciseType, exerciseDuration]
      );
      totalExerciseDuration += exerciseDuration;
      console.log(`Exercise ${i + 1}: ${exerciseType} for ${exerciseDuration} minutes`);
    }
    const healthScore = calculateHealthScore(weight, exerciseCount, totalExerciseDuration, calories);
    await pool.query('UPDATE users SET sentiment = $1 WHERE user_id = $2', [healthScore, userStatId])

    await pool.query('COMMIT');
    res.redirect('/stats');
  } catch (err) {
    await pool.query('ROLLBACK');
    console.error(err);
    res.status(500).send("An error occurred while saving the data");
  }

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
