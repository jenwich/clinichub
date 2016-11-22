import React, { Component } from 'react'

export default function SessionList({sessions, currentSession}) {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">My Sessions</div>
      <div className="list-group">
        {(() => {
          return sessions.map(session => {
            return <a key={session.id} href={'/session/'+ session.id}
              className={"list-group-item" + (session.id == currentSession.id? " active": "")}>{session.topic}</a>
          })
        })()}
      </div>
    </div>
  )
}