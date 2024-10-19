# event-management
Event-management
# Event Management Application

This is an Event Management Application built using FastAPI for the backend and React for the frontend. It allows users to create, join, and leave events in real-time using WebSocket connections.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running the FastAPI Backend](#running-the-fastapi-backend)
  - [Running the React Frontend](#running-the-react-frontend)
- [Why FastAPI?](#why-fastapi)
- [Future Enhancements](#future-enhancements)
- [License](#license)



## Technologies Used

- **Backend**: FastAPI
- **Frontend**: React
- **Database**: SQLite (for testing)
- **WebSocket**: For real-time updates
- **Authentication**: Simple user login
- **Testing**: Pytest for backend testing

## Features

- User registration and login
- Create, join, and leave events
- Real-time updates for event joiners using WebSocket
- Lightweight and easy-to-use architecture

## Why FastAPI?
I had the option to use either FastAPI or Flask for this project. Having already developed a similar application using Flask, I chose FastAPI for the following reasons:

- Lightweight: FastAPI is designed to be efficient and lightweight,    making it an excellent choice for creating APIs.
- Ease of Use: The framework provides a straightforward approach to - building RESTful APIs with minimal boilerplate code.
- Real-Time Updates: FastAPI supports WebSockets natively, allowing for real-time updates for event participants. This was essential for the application's functionality.

## Future Enhancements

- Implement a more robust user interface with advanced features.
- Set up Continuous Integration/Continuous Deployment (CI/CD) for seamless updates.
- Implement JWT token authentication for improved security.
- Enhance WebSocket functionality for more interactive features.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python 3.7+](https://www.python.org/downloads/)
- [Node.js 14+](https://nodejs.org/)
- [npm](https://www.npmjs.com/get-npm) (comes with Node.js)

### Running the FastAPI Backend

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sifykarippery/event-management/tree/main
   cd event-management
   pipenv shell
   pip install -r requirements.txt
   uvicorn app.main:app --reload
### Running the React Frontend

   ```bash
   cd event-management-app
   npm start
