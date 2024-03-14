from apps.rjobs.models.job import Job
from sqlmodel import Session, select


def add_jobs(session: Session, jobs: list[Job]):
    for job in jobs:
        session.add(job)
    session.commit()


def get_all_jobs(session: Session):
    return session.exec(select(Job)).all()
