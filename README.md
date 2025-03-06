# FlashLearn Backend API

## Authors

- Brian Kabaka
- John Gathio
- Stephanie Njonjo

## Description

FlashLearn Backend API is a RESTful API built using Flask for managing decks, flashcards, user authentication, and user progress & statistics. It utilizes JWT authentication to secure protected resources and ensure user data integrity.

## Features

- **User Authentication** (Signup, Login, JWT authentication)
- **Deck Management** (Create, View, Edit, Delete decks)
- **Flashcard Management** (Create, View, Edit, Delete flashcards)
- **Password Hashing** using Flask-Bcrypt
- **JWT-Protected Resources**

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8+
- SQLite database
- Familiarity with Python and Flask

## Installation

Follow these steps to set up and run the backend API:

```bash
# Clone the repository
git clone https://github.com/kabakadev/flashlearn-backend.git

# Navigate into the project directory
cd flashlearn-backend

# Install dependencies using pipenv
pipenv install

# Activate the virtual environment
pipenv shell

# Apply database migrations
flask db upgrade

# Start the Flask development server
flask run
```

## Deployment

The backend API is deployed at:

- [FlashLearn Backend API](https://flashlearn-backend-2.onrender.com)

## Related Repositories

- **Frontend Repository:** [FlashLearn Frontend](https://github.com/kabakadev/flashlearn-frontend.git)
- **Deployed Frontend URL:** [FlashLearn Frontend](https://flashlearn254.netlify.app/)

## API Endpoints

### User Authentication

#### Register a new user

**POST** `/signup`

**Request Body:**

```json
{
  "email": "ian@gmail.com",
  "username": "ian",
  "password": "pussinboots"
}
```

**Response:**

```json
{
  "message": "User registered successfully"
}
```

#### Log in an existing user

**POST** `/login`

**Request Body:**

```json
{
  "email": "ian@gmail.com",
  "password": "pussinboots"
}
```

**Response:**

```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTI4ODI4MSwianRpIjoiNDA1YTliMDQtYWVhZi00Mzg0LWE5MDYtNmZjMjM3M2RkYjMzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwidXNlcm5hbWUiOiJpYW4ifSwibmJmIjoxNzQxMjg4MjgxLCJleHAiOjE3NDEzMTcwODF9.j1A9JH53aaVUmrx82wymZJy5Mi0NesZ86AXR0HTj_VM"
}
```

### Fetch Authenticated User Data

**GET** `/user`

**Response:**

```json
{
  "id": 1,
  "username": "ian"
}
```

### Fetch Logged-in User's Dashboard Data

**GET** `/dashboard`

**Response:**

```json
{
  "username": "ian",
  "total_flashcards_studied": 0,
  "most_reviewed_deck": null,
  "weekly_goal": 0,
  "mastery_level": 0.0,
  "study_streak": 0,
  "focus_score": 0,
  "retention_rate": 0.0,
  "cards_mastered": 0,
  "minutes_per_day": 0.0,
  "accuracy": 0.0,
  "decks": []
}
```
