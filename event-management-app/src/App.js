import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState({
    title: "",
    organizer: "",
    date_time: "",
    duration: 60,
    location: "",
  });

  // WebSocket setup
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      console.log(event.data); // Handle real-time updates
      fetchEvents();
    };

    return () => {
      ws.close();
    };
  }, []);

  const fetchEvents = async () => {
    const response = await axios.get("http://localhost:8000/events/");
    setEvents(response.data);
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const createEvent = async () => {
    try {
      await axios.post("http://localhost:8000/events/", {
        title: newEvent.title,
        organizer: newEvent.organizer,
        date_time: newEvent.date_time,  // Ensure it's a valid ISO datetime string
        duration: parseInt(newEvent.duration, 10),  // Ensure it's an integer
        location: newEvent.location
      });
      setNewEvent({
        title: "",
        organizer: "",
        date_time: "",
        duration: 60,
        location: ""
      });
      fetchEvents();  // Refresh event list after creation
    } catch (error) {
      console.error("Error creating event:", error);
    }
  };
  const joinEvent = async (eventId) => {
    try {
        const payload = { user: "John Doe" };  // Replace with actual user information
        await axios.put(`http://localhost:8000/events/${eventId}/join`, payload);
        fetchEvents();  // Refresh the list of events
    } catch (error) {
        console.error("Error joining event:", error);
    }
};
const unjoinEvent = async (eventId) => {
  try {
    const payload = { user: "John Doe" }; // Replace with the actual user name
    await axios.put(`http://localhost:8000/events/${eventId}/unjoin`, payload);
    fetchEvents(); // Refresh the list of events
  } catch (error) {
    console.error("Error unjoining event:", error);
  }
};

const cancelEvent = async (eventId) => {
  try {
    await axios.delete("http://localhost:8000/events/cancel", {
      data: { event_id: eventId },
    });
    fetchEvents(); // Refresh the list of events
  } catch (error) {
    console.error("Error cancelling event:", error);
  }
};


  return (
    <div>
      <h1>Event Management</h1>

      <h2>Create Event</h2>
      <input
        type="text"
        placeholder="Title"
        value={newEvent.title}
        onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
      />
      <input
        type="text"
        placeholder="Organizer"
        value={newEvent.organizer}
        onChange={(e) =>
          setNewEvent({ ...newEvent, organizer: e.target.value })
        }
      />
      <input
        type="datetime-local"
        value={newEvent.date_time}
        onChange={(e) => setNewEvent({ ...newEvent, date_time: e.target.value })}
      />
      <input
        type="text"
        placeholder="Location"
        value={newEvent.location}
        onChange={(e) =>
          setNewEvent({ ...newEvent, location: e.target.value })
        }
      />
      <button onClick={createEvent}>Create Event</button>

      <h2>Events</h2>
      <ul>
        {events.map((event) => (
          <li key={event.id}>
            <h3>{event.title}</h3>
            <p>Organizer: {event.organizer}</p>
            <p>Date: {event.date_time}</p>
            <p>Location: {event.location}</p>
            <p>Duration: {event.duration} minutes</p>
            <p>Joiners: {event.joiners.join(", ")}</p>
            <button onClick={() => joinEvent(event.id)}>Join Event</button>
            <button onClick={() => unjoinEvent(event.id)}>Leave Event</button>
            <button onClick={() => cancelEvent(event.id)}>Cancel Event</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
