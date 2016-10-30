import React from 'react'
import ReactDOM from 'react-dom'
import { autorun } from 'mobx'
import { myFetch } from '../utils'

import SessionCreator from './components/SessionCreator'
import SessionCreatorStore from './stores/SessionCreatorStore'

let initialData = {
  step: 1,
  clinics: [],
  balance: window.balance || 12345.67
}

myFetch('/api/get_all_clinics').then(data => {
  initialData.clinics = data.clinics
  init()
})

function init() {
  let store = SessionCreatorStore.fromJS(initialData)
  console.log(store.clinics)

  ReactDOM.render(<SessionCreator store={store} />, document.getElementById('session-creator'))
  window.store = store
}

