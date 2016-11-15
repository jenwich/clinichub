import React from 'react'
import ReactDOM from 'react-dom'
import { autorun } from 'mobx'

import { myFetch } from '../utils'
import ClinicManagerStore from './stores/ClinicManagerStore'
import ClinicManager from './components/ClinicManager'

let initialData = {
  page: 'edit', // edit, invite, leave
  clinicId: window.clinicId || '58151bc65a95ef28bb6567f3',
  doctorId: window.doctorId || '580f6de35a95ef3bbb446033',
}

init()

function init() {
  let store = ClinicManagerStore.fromJS(initialData)
  window.store = store
  ReactDOM.render(<ClinicManager store={store} />, document.getElementById('clinic-manager'))
}
