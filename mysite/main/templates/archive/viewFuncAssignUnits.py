# Code I was working on to test assigning units

def test(request):
    project = get_object_or_404(project_model, project_name="Test Project")

    if request.method == "POST":
        # pass the project so the form can filter unit.queryset
        form = UnitAssignmentForm(request.POST, project=project)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.project = project          # tie it to the parent
            assignment.assigned_by = request.user # optional bookkeeping
            assignment.save()
            return redirect("project_detail", project_id=project.id)
    else:
        # GET request – empty form (or pre-select a coder if you like)
        form = UnitAssignmentForm(project=project)

    favorite_list = favorite_projects_list(request.user)
    sys_admin = sys_admin_test(request.user)
    context = {
        'project': project,
        'favorite_list': favorite_list,
        'sys_admin': sys_admin,
    }
    
    return render(request, 'main/test.html', context)