from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, QueryDict, HttpResponse
from rest_framework import viewsets
from .serialiers import PostSerializer
from .forms import PostForm
from .models import Post
# Create your views here.


def post_list(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return JsonResponse(post)
        return JsonResponse(form.errors)

    else:
        return JsonResponse(Post.objects.all())


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'PUT':
        put_data = QueryDict(request.body)
        form = PostForm(put_data, instance=post)
        if form.is_valid():
            post = form.save()
            return JsonResponse(post)
        return JsonResponse(form.errors)
    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse
    else:
        return JsonResponse(post)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
