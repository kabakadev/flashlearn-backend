# FlashLearn Backend API Documentation

## Authors

- Ian Kabaka
- John Gaitho
- Stephanie Njonjo

## Description

FlashLearn is a RESTful API built using Flask for managing decks, flashcards, user authentication, and user progress and statistics. It uses JWT authentication to secure resources.

## Features

- User authentication (Signup, Login, JWT authentication)
- Create, view, edit, and delete decks
- Create, view, edit, and delete flashcards
- Flask Bcrypt for password hashing
- JWT authentication for protected resources

## Prerequisites

- Familiarity with Python
- Python 3.8 and above installed
- SQLite database

## Installation

```sh
# Clone the repository
git clone https://github.com/kabakadev/flashlearn-backend.git

# Navigate into the repository
cd flashlearn-backend

# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Apply database migrations
flask db upgrade

# Start the server
flask run
```

## Deployed Backend URL

[FlashLearn Backend](https://flashlearn-backend-2.onrender.com)

## Related Repositories

- [Frontend Repository](https://github.com/kabakadev/flashlearn-frontend.git)
- [Deployed Frontend](https://flashlearn254.netlify.app/)

## API Endpoints

### Auth Routes

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
  "token": "<JWT_TOKEN>"
}
```

#### Fetch authenticated user data

**GET** `/user`
**Response:**

```json
{
  "id": 1,
  "username": "ian"
}
```

### Dashboard Routes

#### Fetch logged-in user's dashboard data

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

### Deck Routes

#### Create a new deck

**POST** `/decks`
**Request Body:**

```json
{
  "title": "a simple deck",
  "description": "creating a demo deck",
  "subject": "english",
  "category": "demo",
  "difficulty": 1,
  "user_id": 1
}
```

**Response:**

```json
{
  "id": 1,
  "title": "a simple deck",
  "description": "creating a demo deck",
  "subject": "english",
  "category": "demo",
  "difficulty": 1,
  "user_id": 1,
  "created_at": "2025-03-07T07:47:21",
  "updated_at": "2025-03-07T07:47:21"
}
```

#### Get all decks

**GET** `/decks`
**Response:**

```json
[
  {
    "id": 1,
    "title": "a simple deck",
    "description": "creating a demo deck",
    "subject": "english",
    "category": "demo",
    "difficulty": 1,
    "created_at": "2025-03-07T07:47:21",
    "updated_at": "2025-03-07T07:47:21"
  }
]
```

#### Retrieve a single deck by ID

**GET** `/decks/<deck_id>`
**Response:**

```json
{
  "id": 1,
  "title": "a simple deck",
  "description": "creating a demo deck",
  "subject": "english",
  "category": "demo",
  "difficulty": 1,
  "created_at": "2025-03-07T07:47:21",
  "updated_at": "2025-03-07T07:47:21"
}
```

#### Update an existing deck

**PUT** `/decks/<deck_id>`
**Request Body:**

```json
{
  "title": "updated deck",
  "description": "creating a demo deck and updating it",
  "subject": "english update",
  "category": "demo update",
  "difficulty": 3,
  "user_id": 1
}
```

**Response:**

```json
{
  "id": 1,
  "title": "updated deck",
  "description": "creating a demo deck and updating it",
  "subject": "english update",
  "category": "demo update",
  "difficulty": 3,
  "updated_at": "2025-03-07T07:58:01"
}
```

#### Delete a deck

**DELETE** `/decks/<deck_id>`
**Response:**

```json
{
  "message": "Deck deleted successfully"
}
```

### Flashcard Routes

#### Create a new flashcard

**POST** `/flashcards`
**Request Body:**

```json
{
  "deck_id": 1,
  "front_text": "What is 1 + 1",
  "back_text": "2"
}
```

**Response:**

```json
{
  "id": 1,
  "deck_id": 1,
  "front_text": "What is 1 + 1",
  "back_text": "2",
  "created_at": "2025-03-07T08:06:58",
  "updated_at": "2025-03-07T08:06:58"
}
```

#### Retrieve all flashcards

**GET** `/flashcards`
**Response:**

```json
[
  {
    "id": 1,
    "deck_id": 1,
    "front_text": "What is 1 + 1",
    "back_text": "2",
    "created_at": "2025-03-07T08:06:58",
    "updated_at": "2025-03-07T08:06:58"
  }
]
```

#### Update a flashcard

**PUT** `/flashcards/<id>`

```json
{
  "front_text": "What is 1 + 4",
  "back_text": "5"
}
```

#### Delete a flashcard

**DELETE** `/flashcards/<id>`

```json
{
  "message": "Flashcard deleted successfully"
}
```
