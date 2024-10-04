import dotenv from 'dotenv'
import process from 'node:process'
import express from 'express'
import dns from 'node:dns'

import { getDirname } from './utils/dirname.js'
import { setupMiddleware } from './src/middlewares.js'
import { setupRoutes } from './src/routes.js'

dns.setDefaultResultOrder('ipv4first')

dotenv.config()

const env = process.env
const port = env.PORT || 5000
const app = express()
const __dirname = getDirname(import.meta.url)

setupMiddleware(app, __dirname)
setupRoutes(app)

// 404 page
app.use((req, res) => {
  res.status(404).send('404 noob :D')
})

app.listen(port, () => {
  console.log(`Server is running on port http://localhost:${port}`)
})
