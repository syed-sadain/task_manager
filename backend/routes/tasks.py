from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend import db
from backend.models import Task

tasks_bp = Blueprint("tasks", __name__)

VALID_STATUSES = ["Pending", "In Progress", "Completed"]


def _parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


# ── GET /api/tasks ────────────────────────────────────────────────────────────
@tasks_bp.route("", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    status = request.args.get("status", "").strip()
    search = request.args.get("search", "").strip()

    query = Task.query.filter_by(user_id=user_id)

    if status and status in VALID_STATUSES:
        query = query.filter_by(status=status)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify({"tasks": [t.to_dict() for t in tasks], "count": len(tasks)}), 200


# ── POST /api/tasks ───────────────────────────────────────────────────────────
@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data    = request.get_json(silent=True) or {}

    title  = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    status = data.get("status", "Pending")
    if status not in VALID_STATUSES:
        return jsonify({"error": f"status must be one of {VALID_STATUSES}"}), 400

    task = Task(
        title       = title,
        description = (data.get("description") or "").strip() or None,
        due_date    = _parse_date(data.get("due_date")),
        status      = status,
        user_id     = user_id,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created", "task": task.to_dict()}), 201


# ── GET /api/tasks/<id> ───────────────────────────────────────────────────────
@tasks_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())
    task    = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    return jsonify({"task": task.to_dict()}), 200


# ── PUT /api/tasks/<id> ───────────────────────────────────────────────────────
@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task    = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    data    = request.get_json(silent=True) or {}

    if "title" in data:
        title = data["title"].strip()
        if not title:
            return jsonify({"error": "title cannot be empty"}), 400
        task.title = title

    if "description" in data:
        task.description = (data["description"] or "").strip() or None

    if "due_date" in data:
        task.due_date = _parse_date(data["due_date"])

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return jsonify({"error": f"status must be one of {VALID_STATUSES}"}), 400
        task.status = data["status"]

    task.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Task updated", "task": task.to_dict()}), 200


# ── DELETE /api/tasks/<id> ────────────────────────────────────────────────────
@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task    = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200


# ── GET /api/tasks/stats ──────────────────────────────────────────────────────
@tasks_bp.route("/stats", methods=["GET"])
@jwt_required()
def task_stats():
    user_id = int(get_jwt_identity())
    base    = Task.query.filter_by(user_id=user_id)

    stats = {
        "total":       base.count(),
        "pending":     base.filter_by(status="Pending").count(),
        "in_progress": base.filter_by(status="In Progress").count(),
        "completed":   base.filter_by(status="Completed").count(),
    }
    return jsonify({"stats": stats}), 200
