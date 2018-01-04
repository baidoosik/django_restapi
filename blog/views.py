from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, QueryDict, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
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


# APIVIEW 활용해서 api 응답 만들기


class PostListAPIView(APIView):
    # POST요청을 받기 위해 별도로 csrf_exempt 처리를 해줄 필요가 없습니다.
    # APIView.as_view()에서 이미 csrf_exempt처리된 뷰를 만들어주고 있기 때문입니다
    def get(self, request):
        serializer = PostSerializer(Post.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostDetailView(APIView):
    def get_object(selfs, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=204)

# api_view 장식자를 이용하는 api 응답 작성
# api_view는 django-rest-framework 규격의 fbv 를 세팅해주는 장식자


@api_view(['GET'], ['POST'])
def post_list(request):
    if request.method == 'GET':
        serializer = PostSerializer(Post.objects.all(), many=True)
        return Response(serializer.data)
    else:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    else:
        post.delete()
        return Response(status=204)
