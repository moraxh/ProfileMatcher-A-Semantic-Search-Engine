import { Router } from 'express'
import { RegistersController } from './registersController.js'

export const registerRoutes = Router()

registerRoutes.get('/', RegistersController.view)
registerRoutes.get('/all', RegistersController.getAll)
registerRoutes.get('/search', RegistersController.search)
registerRoutes.post('/', RegistersController.insert)
registerRoutes.patch('/:id', RegistersController.update)
registerRoutes.delete('/:id', RegistersController.delete)
