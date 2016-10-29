import React, { Component } from 'react'
import moment from 'moment'

let modifyMessage = (msg, sender) => {
  if (sender == 'D') {
    if (msg.match(/^\/create-transcript/)) {
      return (
        <span>Create&nbsp; 
          <a href={"/transcript/"+ msg.split(' ')[1]}>Transcript</a>
        </span>
      )
    }
  }
  return msg
}

let MessageBox = ({msg, sender, sender_name, time, side}) => {
  return (
    <div className={side} style={{'marginButtom': '10px'}}>
      <big>{modifyMessage(msg, sender)}</big><br />
      <b>{sender_name}</b>
      <small>{time.format('ddd, DD MMM YYYY HH:mm')}</small>
    </div>
  )
}

export default class Message extends Component {
  sendMessage() {
    this.props.sendMessage(this.refs.messageBox.value.trim())
  }

  render() {
    let { session, me } = this.props
    let MessageList = session.messages.map((item, index) => {
      let side = ((item.sender == 'P' && me == 'patient') ||
        (item.sender == 'D' && me == 'doctor'))? 'right': 'left'
      return (
        <MessageBox
          key={index}
          msg={item.msg}
          sender={item.sender}
          sender_name={item.sender=='P'? session.patient.name: session.doctor.name}
          side={side}
          time={moment.unix(item.time)}/>
      )
    })
    return (
      <div>
        <div id="message-list">{MessageList}</div>
        <hr />
        <div className="form-inline" style={{'textAlign': 'center'}}>
          <div className="form-group">
            <label>
              <span>Message:</span>
              <input type="text" ref="messageBox" className="form-control" />
            </label>
          </div>
          <button className="btn btn-primary"
            onClick={this.sendMessage.bind(this)}>Send</button>
          <button className="btn btn-default"
            onClick={this.props.fetchSession}>Refresh</button>
        </div>
        <hr />
        <div>
          {(shouldShow => {
            if (shouldShow) return (
              <div style={{'textAlign': 'center'}}>
                <button className="btn btn-default"
                  onClick={this.props.changePage.bind(null, 'transcript')}>Create Transcript</button>
                <button className="btn btn-default">Create Appointment</button>
                <button className="btn btn-danger">Delete Session</button>
              </div>
            )
          })(me == 'doctor')}
        </div>
      </div>
    )
  }
}
