from django.http.request import HttpRequest
from django.http.response import HttpResponse
from posts.models import Post

def hello_world(request: HttpRequest):
    return HttpResponse("<h1>Hello world!</h1>")

def post_list(request: HttpRequest):
    posts = Post.objects.filter(is_active=True)  # только активные
    final_response = ""

    for post in posts:
        final_response += f"POST TITLE: <h1>{post.title}</h1> CREATED_AT: {post.created_at.strftime('%Y-%m-%d')}<br>"

    return HttpResponse(final_response)
