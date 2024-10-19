import React, { useEffect, useState } from "react";
import axios from "axios";
import Registration from "./components/Registration";

const App = () => {
  const [events, setEvents] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [socket, setSocket] = useState(null);
  const [newEvent, setNewEvent] = useState({ title: "", location: "", dateTime: "", duration: "" });

  useEffect(() => {
    axios.get("http://localhost:8000/events/").then((response) => {
      setEvents(response.data);
    });

    const ws = new WebSocket("ws://localhost:8000/ws");
    setSocket(ws);

    return () => {
      if (ws) ws.close();
    };
  }, []);

  useEffect(() => {
    if (socket) {
      socket.onmessage = (event) => {
        const updatedEvent = JSON.parse(event.data);
        setEvents((prevEvents) => {
          if (updatedEvent.event_id) {
            if (updatedEvent.title) {
              return [...prevEvents, updatedEvent];
            } else {
              return prevEvents.map((ev) =>
                ev.id === updatedEvent.event_id
                  ? { ...ev, joiners: updatedEvent.joiners }
                  : ev
              );
            }
          }
          return prevEvents;
        });
      };
    }
  }, [socket]);

  const createEvent = async () => {
    if (currentUser) {
      const eventDetails = {
        title: newEvent.title,
        location: newEvent.location,
        date_time: newEvent.dateTime,
        duration: newEvent.duration,
      };

      try {
        const response = await axios.post("http://localhost:8000/events/", {
          event: eventDetails,
          user_id: currentUser.id,
        });
        console.log(response.data);
      } catch (error) {
        console.error("Error creating event:", error.response.data);
      }
    } else {
      alert("Please log in to create an event.");
    }
  };

  const handleLogin = () => {
    axios.post("http://localhost:8000/login", { username, password })
      .then((response) => {
        setCurrentUser(response.data);
        localStorage.setItem("user", JSON.stringify(response.data));
      }).catch((error) => {
        console.error("Login error", error);
      });
  };

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setCurrentUser(JSON.parse(storedUser));
    }
  }, []);

  const joinEvent = (eventId) => {
    if (currentUser) {
      axios.post(`http://localhost:8000/events/${eventId}/join`, { user_id: currentUser.id })
        .then((response) => {
          console.log(response.data.message);
        })
        .catch((error) => {
          console.error("Error joining event:", error);
        });
    } else {
      alert("Please log in to join an event.");
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem("user");
  };

  const leaveEvent = (eventId) => {
    if (currentUser) {
      axios.post(`http://localhost:8000/events/${eventId}/leave`, { user_id: currentUser.id })
        .then((response) => {
          // Event will be updated via WebSocket, no need to manually update
        }).catch((error) => {
          console.error("Error leaving event:", error);
        });
    } else {
      alert("Please log in to leave an event.");
    }
  };

  return (
    <div>
      <h1>Event List</h1>

      {!currentUser && (
        <div>
          <h2>Login</h2>
          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
        </div>
      )}

      {currentUser && (
        <div>
          <h2>Welcome, {currentUser.username}!</h2>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}

      {!currentUser && <Registration />}

      {currentUser && (
        <div>
          <h2>Create Event</h2>
          <input
            type="text"
            placeholder="Event Title"
            value={newEvent.title}
            onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
          />
          <input
            type="text"
            placeholder="Location"
            value={newEvent.location}
            onChange={(e) => setNewEvent({ ...newEvent, location: e.target.value })}
          />
          <input
            type="datetime-local"
            value={newEvent.dateTime}
            onChange={(e) => setNewEvent({ ...newEvent, dateTime: e.target.value })}
          />
          <input
            type="number"
            placeholder="Duration (minutes)"
            value={newEvent.duration}
            onChange={(e) => setNewEvent({ ...newEvent, duration: e.target.value })}
          />
          <button onClick={createEvent}>Create Event</button>
        </div>
      )}

      {currentUser ? (
        <div>
          {events.map((event) => (
            <div key={event.id}>
              <h2>{event.title}</h2>
              <p>Location: {event.location}</p>
              <p>Organizer: {event.organizer.username}</p>
              <p>Duration: {event.duration}</p>
              <p>Date: {event.date_time}</p>
              <p>Joiners: {event.joiners.join(", ")}</p>
              <p>
                <button onClick={() => joinEvent(event.id)}>Join</button>
                <button onClick={() => leaveEvent(event.id)}>Leave</button>
              </p>
            </div>
          ))}
        </div>
      ) : (
        <p>Please log in to view events.</p>
      )}
    </div>
  );
};

export default App;
