import { registerRoutes } from './registers/registerRoutes.js'

export const setupRoutes = (app) => {
  app.get('/', (req, res) => {
    res.render('pages/index', { title: 'ProfileMatcher' })
  })

  app.use('/registers', registerRoutes)
}
