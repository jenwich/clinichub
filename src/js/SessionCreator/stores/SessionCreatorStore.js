import { observable, computed, action, toJS } from 'mobx'
import _ from 'lodash'
import fetch from 'isomorphic-fetch'

function getFakeData(data) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(data)
    }, 1000)
  })
}

export default class SessionCreatorStore {
  @observable step = 1
  @observable fieldFilter = ""
  @observable selectedField
  @observable selectedClinic
  @observable completedSession = {
    session_id: 1,
    topic: 'Untitled',
    doctor: {
      name: 'Unnamed',
      field: 'Unfield',
      clinic_name: 'UnnamedClinic'
    }
  }
  clinics = []
  fields = []

  @computed get selectedFields() {
    return this.fields.filter(item => item.toLowerCase().match(this.fieldFilter.toLowerCase()))
  }

  @computed get title() {
    switch (this.step) {
      case 1: return "Step 1: Press the request button"  
      case 2: return "Step 2: Select field"  
      case 3: return "Step 3: Select clinic"  
      case 4: return "Step 4: Review payment method"  
      case 5: return "Step 5: Detail session"  
      case 6: return "Step 6: Finish!"  
    }
  }

  @computed get clinicsWithSelectedField() {
    return this.clinics.filter(item => _.includes(item.fields, this.selectedField))
  }

  deriveFields() {
    this.fields = _.uniq(this.clinics.reduce((prev, curr) => _.union(prev, curr.fields), [])).sort()
  }

  submitSession() {
    let summary = {
      topic: this.sessionTopic,
      description: this.sessionDescription,
      clinic: this.selectedClinic.id,
      field: this.selectedField
    }
    if (!process.env.NODE_ENV) summary.patient = '5808aae05a95ef4211820cbd'
    fetch('http://localhost:8000/api/create_session', {
      header: {
        'content-type': 'applicatino/json'
      },
      method: 'POST',
      body: JSON.stringify(summary)
    }).then(res => {
      if (res.status >= 400) {
        throw new Error("Bad response from server");
      }
      return res.json()
    }).then(data => {
      this.completedSession = Object.assign(this.completedSession, {
        session_id: data.session.id,
        topic: data.session.topic,
        doctor: {
          name: data.doctor.name,
          field: data.doctor.field,
          clinic_name: data.clinic.name
        }
      })
      this.step++;
    })
  }

  static fromJS(data) {
    const store = new SessionCreatorStore()
    store.step = data.step
    store.clinics = data.clinics
    store.deriveFields()
    return store
  }
}
