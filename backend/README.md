# Instagram Scraper REST API

This project is a REST API designed to scrape data from Instagram, focusing on retrieving user information, user posts, and user stories. The API is built using Python, Flask, and SQLAlchemy ORM, providing endpoints for inserting and retrieving data related to Instagram users, their posts, and their stories.

## Features

- **User Data**: Retrieve and store Instagram user information including follower and following.
- **User Posts**: Retrieve and store posts made by users, including post tags.
- **User Stories**: Retrieve and store stories shared by users, including story mentions.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Migration](#database-migration)
- [Testing](#testing)
- [License](#license)

## Installation

To get started with the Instagram Scraper REST API, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/instagram-scraper-api.git
   cd instagram-scraper-api
   ```
2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following:

   ```
   database="ig_scraper"
   userdb="root"
   passdb="123456"
   namauser="abcd123" # username instagram
   password="abc1234" # password instagram
   ```
5. **Run the database migrations**:

   ```bash
   flask db init
   flask db migrate -m "Migration message"
   flask db upgrade
   ```
6. **Start the Flask development server**:

   ```bash
   flask run
   ```

## Requirements

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Migrate
- MySQL (or any other supported database)

## Usage

Once the server is running, you can interact with the API using tools like `curl`, Postman, or any HTTP client.

Example: Create a new user via the API:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "john_doe", "full_name": "John Doe"}' http://localhost:5000/users
```

## API Endpoints

### Users

- **GET /users**: Retrieve all users
- **GET /users/[int:user_id](int:user_id)**: Retrieve a specific user by ID
- **GET /users/username/[string:username](string:username)**: Retrieve a specific user by username

### Posts

- **GET /posts**: Retrieve all posts
- **GET /posts/[int:post_id](int:post_id)**: Retrieve a specific post by ID
- **GET /posts/by_user_pk/[pk]()**: Retrieve all posts by User Pk
- **GET /post_tags**: Retrieve all post tags
- **GET /post_tags/[int:post_id](int:post_id)**: Retrieve all post tags by post ID

### Stories

- **GET /stories**: Retrieve all stories
- **GET /stories/[int:story_id](int:story_id)**: Retrieve a specific story by ID
- **GET /stories/by_user_pk/[pk]()**: Retrieve all stories by User Pk
- **GET /story_mentions**: Retrieve all story mentions
- **GET /story_mentions/by_story_id/[int:story_id]()**: Retrieve all story mentions by story ID

### Count

- **GET /api/count_posts**: Count all posts
- **GET /api/count_users**: Count all users
- **GET /api/count_stories**: Count all stories

### Image

- **GET /post_img/[path:filename](path:filename)**: Get post image by filename
- **GET /profile_img/[path:filename](path:filename)**: Get profile image by filename
- **GET /post_tag_img/[path:filename](path:filename)**: Get post tag image by filename
- **GET /story_img/[path:filename](path:filename)**: Get story image by filename
- **GET /story_mention_img/[path:filename](path:filename)**: Get story mention image by filename

### Scraping

- **POST /scrap**: Scraping Instagram Info by Username
  Body :
  ```
  { "username" : "xxxxx" }
  ```

## Database Migration

To apply database migrations, run the following command:

```bash
flask db upgrade
```

To create a new migration after modifying models:

```bash
flask db migrate -m "Migration message"
flask db upgrade
```

## Testing (not yet)

To run unit tests, execute the following command:

```bash
python -m unittest discover -s tests
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This `README.md` provides a comprehensive overview of the project, installation instructions, and basic usage examples. Adjust the content as needed to fit the specific details and requirements of your project.
