import dotenv from 'dotenv'
import process from 'node:process'
import path from 'node:path'
import express from 'express'
import expressLayouts from 'express-ejs-layouts';

import { getDirname } from './utils/dirname.js'
import { locpath } from './utils/locpath.js'

dotenv.config()

const env       = process.env;
const port      = env.PORT || 5000;
const app       = express();
const __dirname = getDirname(import.meta.url);

// Set Embedded JS View Engine
app.set('view engine', 'ejs');

// Express layouts
app.use(expressLayouts);

// Set EJS View Path
app.set('views', locpath.view(""));

// Serve static files
app.use(express.static(path.join(__dirname, 'public')))

// --------
// Routes
// --------

app.get('/', (req, res) => {
    res.render('pages/index', { title: 'Buscador'})
});

// 404 page
app.use((req, res) => {
    res.status(404).send('404 noob :D');
})

app.listen(port, () => {
    console.log(`Server is running on port http://localhost:${port}`);
});