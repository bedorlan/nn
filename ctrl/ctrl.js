const { createStore } = require('redux')
const zmq = require('zeromq')

const store = createStore(reducer)
const replier = zmq.socket('rep')
const publisher = zmq.socket('pub')

replier.on('message', msg => {
  msg = JSON.parse(msg.toString())
  let response = { ...msg }
  switch (msg.event) {
    case 'get_state':
      response = { ...response, response: store.getState() }
      break

    case 'train': {
      const payload = { trainData: msg.trainData }
      const action = { type: 'TRAIN', payload }
      store.dispatch(action)
      response = { event: response.event }
      break
    }

    case 'stopTrain': {
      const action = { type: 'TRAIN_STOP' }
      store.dispatch(action)
      response = { event: response.event }
      break
    }

    case 'train_result': {
      const payload = { trainResult: msg.content }
      const action = { type: 'TRAIN_RESULT', payload }
      store.dispatch(action)
      break
    }

    default:
      response = { ...response, error: 'nn: unknown event' }
  }

  replier.send(JSON.stringify(response))
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
        trainResult: null,
        train: action.payload.trainData,
      }

    case 'TRAIN_STOP':
      return {
        ...prevState,
        train: undefined,
      }

    case 'TRAIN_RESULT':
      return {
        ...prevState,
        trainResult: action.payload.trainResult,
      }

    default:
      return prevState
  }
}
