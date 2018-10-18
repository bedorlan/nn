const { createStore } = require('redux')
const zmq = require('zeromq')

const store = createStore(reducer)
const replier = zmq.socket('rep')
const publisher = zmq.socket('sub')

replier.on('message', msg => {
  const state = store.getState()
  replier.send(JSON.stringify(state))
})

store.subscribe(state => {
  publisher.send()
})

replier.bind('tcp://*:3001', err => err && console.error(err))
publisher.bind('tcp://*:3002', err => err && console.error(err))

function reducer(prevState, action) {
  if (prevState == null) {
    return {
      models: ['a', 'b'],
    }
  }
  return prevState
}
