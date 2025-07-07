from .models import coding_variable

# Get list of active users favorite projects
def favorite_projects_list(user):
    if user.is_authenticated:
        return user.favorite_projects.all()
    return None

def variable_reorder(project, ids = None):
    if ids:
        print("TRUE")
        # First pass: assign temporary negative ranks to avoid unique constraint collision
        for temp_rank, var_id in enumerate(ids, start=1):
            print(f'temp_rank: {temp_rank}, var_id: {var_id}')
            coding_variable.objects.filter(pk=var_id, variable_project=project).update(variable_rank=-temp_rank)

        # Second pass: assign correct positive ranks
        for final_rank, var_id in enumerate(ids, start=1):
            print(f'final_rank: {final_rank}, var_id: {var_id}')
            coding_variable.objects.filter(pk=var_id, variable_project=project).update(variable_rank=final_rank)
    else:
        print("FALSE")
        # Fetch coding variables from database
        coding_variables = coding_variable.objects.filter(variable_project=project).order_by('variable_rank')

        print("After First fetch:")
        for var in coding_variables:
            print(f"var: {var.variable_rank:<3} {var.variable_id:<3} {var.variable_name:<20}")

        # First pass: assign temporary negative ranks to avoid unique constraint collision
        for temp_rank, variable in enumerate(coding_variables, start=1):
            coding_variable.objects.filter(pk=variable.pk, variable_project=project).update(variable_rank=-temp_rank)

        print("After First pass:")
        for var in coding_variables:
            print(f"var: {var.variable_rank:<3} {var.variable_id:<3} {var.variable_name:<20}")

        # Fetch updated coding variables from database
        coding_variables = coding_variable.objects.filter(variable_project=project).order_by('variable_id')

        print("After Second fetch:")
        for var in coding_variables:
            print(f"var: {var.variable_rank:<3} {var.variable_id:<3} {var.variable_name:<20}")

        # Second pass: assign correct positive ranks
        for final_rank, variable in enumerate(coding_variables, start=1):
            coding_variable.objects.filter(pk=variable.pk, variable_project=project).update(variable_rank=final_rank)

        print("After Second pass:")
        for var in coding_variables:
            print(f"var: {var.variable_rank:<3} {var.variable_id:<3} {var.variable_name:<20}")

        # Fetch updated coding variables from database
        coding_variables = coding_variable.objects.filter(variable_project=project).order_by('variable_rank')

        print("After Third fetch:")
        for var in coding_variables:
            print(f"var: {var.variable_rank:<3} {var.variable_id:<3} {var.variable_name:<20}")