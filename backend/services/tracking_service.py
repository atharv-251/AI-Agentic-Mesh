from sqlalchemy.orm import Session

from backend.models import KTSession, KTTrackingActivity


def sync_session_activities(transition_id: str, activities: list[KTTrackingActivity], db: Session) -> None:
    tracked_session_ids = {activity.session_id for activity in activities}
    sessions = db.query(KTSession).filter_by(transition_id=transition_id).order_by(KTSession.scheduled_date, KTSession.start_time).all()
    for session in sessions:
        if session.id in tracked_session_ids:
            continue
        db.add(KTTrackingActivity(
            transition_id=transition_id, session_id=session.id,
            activity_name=session.session_title,
            status="completed" if session.status == "completed" else "planned",
            progress_percent=100 if session.status == "completed" else 0,
            expected_topics=[session.session_title],
        ))
