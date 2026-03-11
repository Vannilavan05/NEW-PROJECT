
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

mongoose.connect("mongodb://localhost:27017/lms");

app.get("/", (req, res) => {
  res.send("LMS Backend Running");
});

app.listen(5000, () => {
  console.log("Server running on port 5000");
});
