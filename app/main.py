import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Integer, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./tasks.db')
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {})

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

class TaskUpdate(BaseModel):
    completed: bool

class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool
    model_config = {'from_attributes': True}

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title='TaskFlow API', lifespan=lifespan)
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/')
def index():
    return FileResponse('static/index.html')

@app.get('/health')
def health():
    with engine.connect() as conn:
        conn.exec_driver_sql('SELECT 1')
    return {'status': 'ok'}

@app.get('/api/tasks', response_model=list[TaskOut])
def list_tasks():
    with Session(engine) as session:
        return session.scalars(select(Task).order_by(Task.id.desc())).all()

@app.post('/api/tasks', response_model=TaskOut, status_code=201)
def add_task(data: TaskCreate):
    with Session(engine) as session:
        task = Task(title=data.title.strip())
        if not task.title:
            raise HTTPException(422, 'Title cannot be blank')
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.patch('/api/tasks/{task_id}', response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            raise HTTPException(404, 'Task not found')
        task.completed = data.completed
        session.commit()
        session.refresh(task)
        return task

@app.delete('/api/tasks/{task_id}', status_code=204)
def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            raise HTTPException(404, 'Task not found')
        session.delete(task)
        session.commit()
