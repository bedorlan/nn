const fs = require('fs')
const { EventEmitter } = require('events')
const { promisify } = require('util')
const express = require('express')
const bodyParser = require('body-parser')
const zmq = require('zeromq')

fs.readdir = promisify(fs.readdir).bind(fs)
setTimeout = promisify(setTimeout)

const port = 3000

async function main() {
  const app = express()
  const emitter = new EventEmitter()

  const client = zmq.socket('req')
  client.connect('tcp://ctrl:3001')
  client.on('message', msg => {
    emitter.emit('get_models', { content: msg })
  })

  app.get('/cgi/models', async (req, res) => {
    try {
      client.send('')
      // FIXME: correlation id!
      emitter.once('get_models', msg =>
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

  app.post('/cgi/train', (req, res) => {
    const { body } = req
    if (!body.trainData) {
      console.error(400, body)
      res.sendStatus(400)
      return
    }

    const content = JSON.stringify(body)
    // TODO
    res.status(200).send('{}')
  })

  app.listen(port, () => console.log(`Example app listening on port ${port}!`))
}

main().catch(err => console.error(err))
