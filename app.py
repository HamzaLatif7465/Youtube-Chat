from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
from models import User
import trans1 as tn  # assuming this handles YouTube and LLM logic

# Initialize DB
Base.metadata.create_all(bind=engine)

# App setup
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
templates = Jinja2Templates(directory="templates")

# Global variable
embed_code = ""


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Main Page ----------------
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "title": "FastAPI Home"})


@app.post("/")
async def post_form(video_url: str = Form(...)):
    global embed_code
    embed_code = video_url.split("v=")[1]  # Extract YouTube ID
    return RedirectResponse(url=f"/chatpage?video_url={video_url}", status_code=303)


# ---------------- Chat Page ----------------
@app.get("/chatpage", response_class=HTMLResponse)
async def say_hello(request: Request, video_url: str = ""):
    return templates.TemplateResponse("chatpage.html", {
        "request": request,
        "title": "FastAPI Chat page",
        "video_url": video_url,
        "url": video_url
    })


@app.post("/chatpage", response_class=HTMLResponse)
async def post_question(request: Request, question: str = Form(...)):
    try:
        retriever = tn.get_video_embed(embed_code)
        output = tn.llm_call(question, retriever)
    except Exception as e:
        print(f"Error during LLM call: {e}")
        output = "An error occurred while processing your request."

    return templates.TemplateResponse("partials/result.html", {
        "request": request,
        "result": output
    })


# ---------------- Sign In ----------------
@app.get("/signin", response_class=HTMLResponse)
def signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request, "title": "FastAPI Signin"})


@app.post("/signin")
async def post_signin(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if user and user.password == password:
        request.session["user_id"] = user.id
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse("signin.html", {
        "request": request,
        "error": "Invalid credentials"
    })


# ---------------- Sign Up ----------------
@app.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup", response_class=HTMLResponse)
async def post_signup(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password1: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db)
):
    if password1 != password2:
        return HTMLResponse("<h3 style='color:red;'>Passwords do not match!</h3>")

    user = db.query(User).filter(User.email == email).first()
    if user:
        return HTMLResponse("<h3 style='color:red;'>User already registered!</h3>")

    new_user = User(name=name, email=email, password=password1)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse("/", status_code=302)


# ---------------- Logout ----------------
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/signin", status_code=302)


# ---------------- Update User Profile ----------------
@app.get("/update", response_class=HTMLResponse)
async def get_update(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/signin")

    user = db.query(User).filter(User.id == user_id).first()
    return templates.TemplateResponse("updates.html", {"request": request, "user": user})


@app.post("/update", response_class=HTMLResponse)
async def post_update(
    request: Request,
    name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/signin")

    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = name
        user.password = password
        db.commit()

    return RedirectResponse("/", status_code=302)
