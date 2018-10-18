const { createStore } = require('redux')
const zmq = require('zeromq')

const store = createStore(reducer)
const replier = zmq.socket('rep')
const publisher = zmq.socket('pub')

replier.on('message', msg => {
  msg = JSON.parse(msg.toString())
  let content = { ...msg }
  switch (msg.event) {
    case 'get_state':
      content = { ...content, response: store.getState() }
      break

    case 'train': {
      const payload = { trainData: msg.trainData }
      const action = { type: 'TRAIN', payload }
      store.dispatch(action)
      content = { event: content.event }
      break
    }

    case 'train_result': {
      console.log('new train_result', content)
      break
    }

    default:
      content = { ...content, error: 'nn: unknown event' }
  }

  replier.send(JSON.stringify(content))
})

store.subscribe(() => {
  const state = store.getState()
  console.log('new_state', state)
  publisher.send(JSON.stringify(state))
})

replier.bind('tcp://*:3001', err => err && console.error(err))
publisher.bind('tcp://*:3002', err => err && console.error(err))

function reducer(prevState, action) {
  console.log('reducer', prevState, action)

  if (prevState == null) {
    return {
      models: ['a', 'b'],
    }
  }

  switch (action.type) {
    case 'TRAIN':
      return {
        ...prevState,
        train: action.payload.trainData,
      }

    default:
      return prevState
  }
}
