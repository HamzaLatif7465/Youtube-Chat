===============================================================
   FastAPI YouTube Transcript Chat App with Authentication
===============================================================

This is a full-stack web application built using FastAPI that lets users chat with a YouTube video transcript. It includes:

- Sign-Up
- Sign-In
- Update Profile
- Logout

All user data is stored in a SQL database (SQLite), and the system includes a basic session-based authentication mechanism.

---------------------------------------------------------------
Features
---------------------------------------------------------------
✔ Sign Up and Log In (with email and password)  
✔ Update user profile  
✔ Logout button to end session  
✔ Input a YouTube video URL  
✔ Ask questions about the video transcript  
✔ Uses an LLM model (defined in trans1.py) to generate answers  
✔ HTML templates powered by Jinja2  
✔ Clean URL routing with FastAPI

---------------------------------------------------------------
Tech Stack
---------------------------------------------------------------
- Backend: FastAPI
- Frontend: HTML5 with Jinja2 templates
- Database: SQLite (via SQLAlchemy ORM)
- Sessions: Starlette Session Middleware
- Language Model Logic: Custom (trans1.py)

---------------------------------------------------------------
How to Run the App
---------------------------------------------------------------

1. Clone this repo:

   git clone https://github.com/HamzaLatif7465/Youtube-Chat.git
   cd Youtube-Chat

2. Install required packages:

   pip install -r requirements.txt

   Example packages include:
   - fastapi
   - uvicorn
   - sqlalchemy
   - jinja2
   - databases

3. Run the FastAPI server:

   uvicorn main:app --reload

   Visit: http://localhost:8000

---------------------------------------------------------------
Project Structure
---------------------------------------------------------------

fastapi-youtube-chat/
│
├── main.py             # Main FastAPI application
├── trans1.py           # Handles transcript and LLM logic
├── database.py         # DB connection and setup
├── models.py           # SQLAlchemy user model
├── templates/
│   ├── main.html
│   ├── signin.html
│   ├── signup.html
│   ├── chatpage.html
│   ├── update.html
│   └── partials/
│       └── result.html
├── static/             # (Optional) CSS/JS
├── users.db            # SQLite DB file
└── README.txt

---------------------------------------------------------------
LLM Transcript Chat Logic
---------------------------------------------------------------

Handled in `trans1.py`. This file includes functions like:

   - get_video_embed(video_url)
   - llm_call(question, retriever)

These work together to retrieve the transcript and generate a response.

---------------------------------------------------------------
Security Notice
---------------------------------------------------------------

⚠ WARNING: Passwords are stored in plain text. Do not use this in production!
✔ For production, use password hashing (bcrypt or passlib).
✔ Also consider using OAuth for better security.

---------------------------------------------------------------
Author
---------------------------------------------------------------

Hamza Latif — AI Developer & Student  
GitHub: https://github.com/HamzaLatif7465 
Email: HamzaLatif7465@gmail.com

