from django.http import HttpResponse
from .dal import users_dal , user_roles_dal


def home(request):
    return HttpResponse("Hello, world. You're at the Bingo Airlines home page hello hello.")

def add_user_view(request):
    user_role = user_roles_dal.get_by_id(1)
    new_user = users_dal.add(
        id="112233445",
        username="testuser",
        password="testpassword",
        email="test@example.com",
        user_role=user_role,
    )


    return HttpResponse(f"New user {new_user.username} created with ID {new_user.id}.")



def show_users(request):
    users = users_dal.get_all()
    output = ', '.join([u.username for u in users])
    return HttpResponse(output)


def update_user(request,pk):
    user = users_dal.get_by_id(pk)
    user = users_dal.update(pk, username="newusername")
    return HttpResponse(f"User {user.id} updated to {user.username}.")