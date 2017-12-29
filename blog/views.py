from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, QueryDict, HttpResponse
from rest_framework import viewsets
from .serialiers import PostSerializer
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm
from .models import Post
# Create your views here.


@csrf_exempt
def post_list(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return HttpResponse(status=201)
        return JsonResponse(form.errors, status=400)

    else:
        data = ({'pk': post.pk, 'message': post.message} for post in Post.objects.all())
        return JsonResponse(data, safe=False)


@csrf_exempt
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'PUT':
        put_data = QueryDict(request.body)
        form = PostForm(put_data, instance=post)
        if form.is_valid():
            post = form.save()
            return JsonResponse(post)
        return JsonResponse(form.errors, status=400)
    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse('', status=204)
    else:
        return JsonResponse({'pk': post.pk, 'mesage': post.message})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
