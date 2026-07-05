from django.utils import timezone


def get_raven_message(
    user,
    active_goals,
    completed_goals,
    active_projects,
    review_completed,
):
    """
    Returns:
        raven_title
        raven_message
    """

    hour = timezone.localtime().hour

    goal_count = active_goals.count()
    project_count = active_projects.count()
    streak = user.streak

    # ----------------------------
    # Highest Priority
    # Daily Review Pending
    # ----------------------------

    if hour >= 18 and not review_completed:

        return (
            "One Final Task",
            "Complete today's Daily Review before ending the day."
        )

    # ----------------------------
    # Streak
    # ----------------------------

    if streak >= 7:

        return (
            "Iron Discipline",
            f"Your streak stands at {streak} days. Protect it."
        )

    # ----------------------------
    # Morning
    # ----------------------------

    if 5 <= hour < 12:

        if goal_count:

            return (
                "Today's Forge Awaits",
                f"You have {goal_count} mission(s). Build momentum early."
            )

        return (
            "Forge Your First Mission",
            "Create your first goal and give today a purpose."
        )

    # ----------------------------
    # Afternoon
    # ----------------------------

    if 12 <= hour < 18:

        if goal_count:

            return (
                "Keep Moving",
                f"{goal_count} mission(s) remain. Stay focused."
            )

        return (
            "Momentum Maintained",
            "Every mission has been forged. Excellent work."
        )

    # ----------------------------
    # Projects
    # ----------------------------

    if project_count:

        return (
            "Builders Never Stop",
            f"{project_count} active project(s) await progress."
        )

    # ----------------------------
    # Default
    # ----------------------------

    return (
        "Keep Forging",
        "Small victories become great achievements through consistency."
    )