import path from 'node:path'
import expressLayouts from 'express-ejs-layouts'
import favicon from 'serve-favicon'
import express from 'express'

import { locpath } from '../utils/locpath.js'

export const setupMiddleware = (app, __dirname) => {
  // Set Embedded JS View Engine
  app.set('view engine', 'ejs')

  // Express layouts
  app.use(expressLayouts)

  // Set EJS View Path
  app.set('views', locpath.view(''))

  // Serve static files
  app.use('/public', express.static(path.join(__dirname, 'public')))

  // Favicon
  app.use(favicon(locpath.public_('favicon.ico')))

  // Body Parser
  app.use(express.json())
}
