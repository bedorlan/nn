const fs = require('fs')
const { EventEmitter } = require('events')
const { promisify } = require('util')
const express = require('express')
const bodyParser = require('body-parser')
const amqp = require('amqplib')

fs.readdir = promisify(fs.readdir).bind(fs)
setTimeout = promisify(setTimeout)

const port = 3000

async function main() {
  let conn
  while (true) {
    try {
      await setTimeout(10 * 1000)
      conn = await amqp.connect('amqp://broker')
      break
    } catch (err) {
      console.error(err)
    }
  }
  const ch = await conn.createChannel()
  const app = express()

  const qModels = await ch.assertQueue('', { exclusive: true })
  const qModelsEv = new EventEmitter()
  ch.consume(qModels.queue, msg => qModelsEv.emit(qModels.queue, msg))
  app.get('/models', async (req, res) => {
    try {
      ch.sendToQueue('get_models', Buffer.from(''), { replyTo: qModels.queue })
      // FIXME: correlation id!
      qModelsEv.once(qModels.queue, msg =>
        res
          .header('Content-type', 'application/json')
          .status(200)
          .send(msg.content),
      )
    } catch (err) {
      console.error(err)
      res.sendStatus(500)
    }
  })

  app.use(bodyParser.json())

  app.post('/train', (req, res) => {
    const { body } = req
    if (!(body.modelName && body.windowSize && body.data)) {
      console.error(400, body)
      res.sendStatus(400)
      return
    }

    // TODO
    res.sendStatus(200)
  })

  app.listen(port, () => console.log(`Example app listening on port ${port}!`))
}

main().catch(err => console.error(err))
