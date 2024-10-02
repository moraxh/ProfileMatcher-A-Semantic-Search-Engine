import { connect2DB } from '../database.js'
import { ObjectId } from 'mongodb'

// Database connection
const client = await connect2DB()
const db = client.db(process.env.DATABASE_NAME)
const collection = db.collection(process.env.DATABASE_COLLECTION)

export class RegistersModel {
  static async getAll () {
    console.log(await collection.find().toArray())
    return await collection.find().toArray()
  }

  static async insert ({ data }) {
    return await collection.insertOne(data)
  }

  static async update ({ id, data }) {
    return await collection.updateOne({ _id: ObjectId.createFromHexString(id) }, { $set: data })
  }

  static async delete ({ id }) {
    return await collection.findOneAndDelete({ _id: ObjectId.createFromHexString(id) })
  }
}
