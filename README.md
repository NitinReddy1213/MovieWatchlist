# Movie Watchlist Web App

## Overview
Movie Watchlist is a Flask-based web application that allows users to create and manage their personal movie watchlists. Users can register, log in, and add, edit, or delete movies from their list.

## Features
- User authentication (register, login, logout)
- Add, edit, and delete movies from the watchlist
- View detailed movie information
- Responsive and user-friendly design

## Project Structure
```
nitinreddy1213-moviewatchlist/
├── __init__.py
├── dependencies.txt
├── forms.py
├── models.py
├── routes.py
├── static/
│   ├── forms.css
│   ├── main.css
│   ├── movie_details.css
│   ├── movies.css
│   └── reset.css
├── templates/
│   ├── index.html
│   ├── layout.html
│   ├── login.html
│   ├── movie_details.html
│   ├── movieform.html
│   ├── new_movie.html
│   ├── register.html
│   └── macros/
│       ├── fields.html
│       ├── footer.html
│       ├── nav.html
│       └── svgs.html
```

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/nitinreddy1213/moviewatchlist.git
   cd moviewatchlist
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r dependencies.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the root directory and configure necessary variables like database URL and secret key.

5. **Run the Application**
   ```bash
   flask run
   ```

6. **Access the App**
   - Open your browser and go to `http://127.0.0.1:5000`

## Usage
- Register or log in to manage your movie watchlist.
- Add movies using the form and view their details.
- Edit or delete movies as needed.

## Technologies Used
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS
- **Database:** mongoDB

## Contributing
Contributions are welcome! Feel free to fork this repository, make changes, and submit a pull request.
