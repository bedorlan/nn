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

  const newStateEvent = 'new_state'
  let prevState = '{}'
  const subscriber = zmq.socket('sub')
  subscriber.connect('tcp://ctrl:3002')
  subscriber.subscribe('')
  subscriber.on('message', msg => {
    prevState = msg = msg.toString()
    console.log('new subscriber message', msg)
    emitter.emit(newStateEvent, msg)
  })

  app.get('/cgi/watch', async (req, res) => {
    try {
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        Connection: 'keep-alive',
      })

      const notifyFn = () => res.write(`data: ${prevState}\n\n`)
      emitter.on(newStateEvent, notifyFn)
      req.on('close', () => emitter.removeListener(newStateEvent, notifyFn))

      if (prevState) {
        notifyFn()
      }
    } catch (err) {
      console.error(err)
      res.sendStatus(500)
    }
  })

  const client = zmq.socket('req')
  client.connect('tcp://ctrl:3001')
  client.on('message', msg => {
    msg = JSON.parse(msg.toString())
    emitter.emit(msg.event, msg.response)
  })

  app.get('/cgi/models', async (req, res) => {
    try {
      const event = 'get_state'
      const content = { event }
      client.send(JSON.stringify(content))
      emitter.once(event, response =>
        res
          .header('Content-type', 'application/json')
          .status(200)
          .send(response),
      )
    } catch (err) {
      console.error(err)
      res.sendStatus(500)
    }
  })

  app.get('/cgi/stopTrain', (req, res) => {
    try {
      console.log('/cgi/stopTrain')
      const event = 'stopTrain'
      const content = { event }
      client.send(JSON.stringify(content))

      emitter.once(event, () => res.sendStatus(202))
    } catch (err) {
      console.error(err)
      res.sendStatus(500)
    }
  })

  app.use(bodyParser.json())

  app.post('/cgi/train', (req, res) => {
    try {
      const { body } = req
      console.log('/cgi/train', body)
      if (!body.trainData) {
        console.error(400, body)
        return res.sendStatus(400)
      }

      const event = 'train'
      const { trainData } = body
      const content = { event, trainData }
      client.send(JSON.stringify(content))

      emitter.once(event, () => res.sendStatus(202))
    } catch (err) {
      console.error(err)
      res.sendStatus(500)
    }
  })

  app.listen(port, () => console.log(`Example app listening on port ${port}!`))
}

main().catch(err => console.error(err))
