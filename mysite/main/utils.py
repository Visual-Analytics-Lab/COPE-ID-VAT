# Get list of active users favorite projects
def favorite_projects_list(user):
    if user.is_authenticated:
        return user.favorite_projects.all()
    return None
