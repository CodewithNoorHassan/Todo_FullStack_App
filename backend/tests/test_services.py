from sqlmodel import SQLModel, create_engine, Session
from backend.models.user import User
from backend.services.todo_service import TodoService
from backend.models.todo import TodoCreate


def test_todo_service_create_and_get():
    # In-memory SQLite for unit testing
    engine = create_engine("sqlite:///:memory:", echo=False)

    # Import models to ensure metadata populated
    from backend.models.task import Task  # noqa: F401

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # create a user
        user = User(email="tester@example.com", name="Tester")
        session.add(user)
        session.commit()
        session.refresh(user)

        # create todo via service
        todo_in = TodoCreate(title="Test Todo", description="Testing")
        todo = TodoService.create_todo(session, user.id, todo_in)

        assert todo.id is not None
        fetched = TodoService.get_todo(session, user.id, todo.id)
        assert fetched is not None
        assert fetched.title == "Test Todo"
