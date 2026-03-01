"""
MongoDB Document Models (reference structure).

Example User Document:
{
    "_id": ObjectId("..."),
    "email": "user@example.com",
    "password": "$2b$12$...",          // bcrypt hashed
    "role": "user",                     // "user" or "admin"
    "name": "John Doe",
    "phone": "+1234567890",
    "address": "123 Main St, City",
    "is_active": true,
    "created_at": "2026-03-01T00:00:00",
    "updated_at": "2026-03-01T00:00:00"
}
"""


def user_helper(user: dict) -> dict:
    """Convert MongoDB document to a serializable dict."""
    return {
        "id": str(user["_id"]),
        "email": user.get("email", ""),
        "role": user.get("role", "user"),
        "name": user.get("name", ""),
        "phone": user.get("phone", ""),
        "address": user.get("address", ""),
        "is_active": user.get("is_active", True),
        "created_at": str(user.get("created_at", "")),
        "updated_at": str(user.get("updated_at", "")),
    }
