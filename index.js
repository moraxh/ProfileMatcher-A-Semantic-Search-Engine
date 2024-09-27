import dotenv from 'dotenv'
import process from 'node:process'
import express from 'express'

dotenv.config()

const env = process.env;
const port = env.PORT || 5000;
const app = express();

// 404 page
app.use((req, res) => {
    res.status(404).send('404 noob :D');
})

app.listen(port, () => {
    console.log(`Server is running on port http://localhost:${port}`);
});