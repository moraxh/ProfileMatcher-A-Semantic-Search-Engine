import { connect2DB } from '../database.js'
import { ObjectId } from 'mongodb'

// Database connection
const client = await connect2DB()
const db = client.db(process.env.DATABASE_NAME)
const collection = db.collection(process.env.DATABASE_COLLECTION)

function processText (text) {
  return new Promise((resolve, reject) => {
    fetch(`http://localhost:${process.env.PYTHON_PORT}/processText?text=${encodeURIComponent(text)}`)
      .then(async response => {
        if (!response.ok) {
          reject(new Error('Error fetching data'))
        }

        resolve(await response.json())
      })
  })
}

export class RegistersModel {
  static async getAll () {
    return await collection.find().toArray()
  }

  static async insert ({ data }) {
    data.description_formatted = await processText(data.description)
    return await collection.insertOne(data)
  }

  static async update ({ id, data }) {
    collection.updateOne({ _id: ObjectId.createFromHexString(id) }, { $set: { description_formatted: await processText(data.description) } })
    return await collection.updateOne({ _id: ObjectId.createFromHexString(id) }, { $set: data })
  }

  static async delete ({ id }) {
    return await collection.findOneAndDelete({ _id: ObjectId.createFromHexString(id) })
  }
}
