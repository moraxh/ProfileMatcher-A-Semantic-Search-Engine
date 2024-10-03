import { RegistersModel } from './registersModel.js'

function cosineSimilarity (vecA, vecB) {
  const dotProduct = vecA.reduce((sum, value, index) => sum + value * vecB[index], 0)
  const magnitudeA = Math.sqrt(vecA.reduce((sum, value) => sum + value * value, 0))
  const magnitudeB = Math.sqrt(vecB.reduce((sum, value) => sum + value * value, 0))

  if (magnitudeA === 0 || magnitudeB === 0) return 0
  return dotProduct / (magnitudeA * magnitudeB)
}

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
    const top = 5
    const { description } = req.query
    const registers = await RegistersModel.getAll()

    // Get the vocabulary
    const descriptions = registers
      .map(register => (register.description).toLowerCase().split(' ')).flat()
      .concat(description)

    const vocabulary = [...new Set(descriptions)]

    const descriptionVector = vocabulary.map(word => descriptions.filter(_word => _word === word).length)

    const scores = registers.map(register => {
      const registerWords = register.description.toLowerCase().split(' ')
      const registerVector = vocabulary.map(word => registerWords.filter(_word => _word === word).length)

      // Calculate the cosine similarity
      const score = cosineSimilarity(descriptionVector, registerVector)

      return { ...register, score }
    })

    // Sort scores by score
    scores.sort((a, b) => b.score - a.score)

    // Send the top 5 results
    res.json(scores.slice(0, top))
  }
}
