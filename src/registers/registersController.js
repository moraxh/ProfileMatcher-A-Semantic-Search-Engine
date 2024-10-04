import { RegistersModel } from './registersModel.js'

export class RegistersController {
  static async view (req, res) {
    res.render('pages/editRegister', { title: 'Edit Registers' })
  }

  static async getAll (req, res) {
    res.json(await RegistersModel.getAll())
  }

  static async insert (req, res) {
    const { data } = req.body
    res.json(await RegistersModel.insert({ data }))
  }

  static async update (req, res) {
    const { id } = req.params
    const { data } = req.body
    res.json(await RegistersModel.update({ id, data }))
  }

  static async delete (req, res) {
    const { id } = req.params
    res.json(await RegistersModel.delete({ id }))
  }

  static async search (req, res) {
    const { description } = req.query
    if (description == null) {
      res.status(400).json({ message: 'Missing description query parameter' })
      return
    }

    console.log(`http://localhost:${process.env.PYTHON_PORT}/search?term=${encodeURIComponent(req.query.description)}&top=5`)
    fetch(`http://localhost:${process.env.PYTHON_PORT}/search?term=${encodeURIComponent(req.query.description)}&top=5`)
      .then(async response => {
        if (!response.ok) {
          res.status(500).json({ message: 'Error fetching data' })
        }

        res.json(await response.json())
      })
  }
}
