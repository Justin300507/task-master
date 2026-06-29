from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.users import User
from app.models.lists import List
from app.models.list_members import ListMember
from app.models.tasks import Task
from app.models.tags import Tag

seed_router = APIRouter()

@seed_router.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    # ----- Users -----
    users_data = [
        {"email": "alex.chen@example.com", "username": "alexc", "display_name": "Alex Chen", "title": "Mr.", "full_name": "Alex Chen"},
        {"email": "maria.garcia@example.com", "username": "mgarcia", "display_name": "Maria Garcia", "title": "Ms.", "full_name": "Maria Garcia"},
        {"email": "james.kim@example.com", "username": "jkim", "display_name": "James Kim", "title": "Mr.", "full_name": "James Kim"},
        {"email": "linda.wong@example.com", "username": "lwong", "display_name": "Linda Wong", "title": "Dr.", "full_name": "Linda Wong"},
        {"email": "ryan.brown@example.com", "username": "rbrown", "display_name": "Ryan Brown", "title": "Mr.", "full_name": "Ryan Brown"},
    ]
    user_objs = {}
    for data in users_data:
        existing = db.query(User).filter(User.email == data["email"]).first()
        if not existing:
            user = User(**data)
            db.add(user)
            try:
                db.commit()
                db.refresh(user)
                user_objs[data["email"]] = user
            except IntegrityError:
                db.rollback()
        else:
            user_objs[data["email"]] = existing

    # ----- Tags -----
    tag_names = ["urgent", "frontend", "backend", "design", "research"]
    tag_objs = {}
    for name in tag_names:
        tag = db.query(Tag).filter(Tag.name.ilike(name)).first()
        if not tag:
            tag = Tag(name=name)
            db.add(tag)
            try:
                db.commit()
                db.refresh(tag)
                tag_objs[name] = tag
            except IntegrityError:
                db.rollback()
        else:
            tag_objs[name] = tag

    # ----- Lists -----
    list_names = ["Project Alpha", "Marketing Campaign", "Product Roadmap"]
    list_objs = {}
    for name in list_names:
        lst = db.query(List).filter(List.name == name).first()
        if not lst:
            lst = List(name=name)
            db.add(lst)
            try:
                db.commit()
                db.refresh(lst)
                list_objs[name] = lst
            except IntegrityError:
                db.rollback()
        else:
            list_objs[name] = lst

    # ----- List Members (add each user to each list) -----
    for lst in list_objs.values():
        for user in user_objs.values():
            exists = db.query(ListMember).filter(
                ListMember.list_id == lst.id,
                ListMember.user_id == user.id,
            ).first()
            if not exists:
                lm = ListMember(list_id=lst.id, user_id=user.id, role="member")
                db.add(lm)
                try:
                    db.commit()
                except IntegrityError:
                    db.rollback()

    # ----- Tasks -----
    tasks_data = [
        {"title": "Launch Q3 campaign", "description": "Prepare all assets and launch plan", "status": "In Progress", "priority": "High", "user_id": user_objs["alex.chen@example.com"].id},
        {"title": "Fix login bug", "description": "Resolve issue causing login failures", "status": "Done", "priority": "Critical", "user_id": user_objs["maria.garcia@example.com"].id},
        {"title": "Design new UI mockups", "description": "Create high‑fidelity mockups for the dashboard", "status": "Todo", "priority": "Medium", "user_id": user_objs["james.kim@example.com"].id},
        {"title": "Set up CI/CD pipeline", "description": "Automate builds and deployments", "status": "Todo", "priority": "High", "user_id": user_objs["linda.wong@example.com"].id},
        {"title": "Research competitor pricing", "description": "Gather data on market rates", "status": "In Progress", "priority": "Low", "user_id": user_objs["ryan.brown@example.com"].id},
    ]
    for td in tasks_data:
        exist = db.query(Task).filter(Task.title == td["title"]).first()
        if not exist:
            task = Task(**td)
            db.add(task)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()

    return {"detail": "seed data inserted"}
