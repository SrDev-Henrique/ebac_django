from django.shortcuts import get_object_or_404, render

from .models import Post


def post(request):
    post_list = Post.objects.all().order_by("-created_on")
    return render(request, "index.html", {"post_list": post_list})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "post_detail.html", {"post": post})
