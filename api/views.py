from django.contrib import auth
from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import NewsPost
from .serializers import NewsListSerializer


# Create your views here.
class UserLoginAPI(APIView):
    def post(self, request):
        """
        User login api
        """
        data = request.data
        try:
            user = auth.authenticate(
                username=data["username"], password=data["password"])
            if user:
                token = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(token),
                    'access_token': str(token.access_token)
                }

                return (Response(data, status=200))
            else:
                return Response({"message": "Not correct username or password"}, status=401)
        except Exception as e:
            return Response({"message": str(e)}, status=401)


class NewsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "limit"
    max_page_size = 100


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsListSerializer
    pagination_class = NewsPagination

    def get_queryset(self):
        return NewsPost.objects.all()

    def get_permissions(self):
        self.permission_classes = [permissions.IsAuthenticated]
        if self.action in ["list", "retrieve", "search"]:
            self.permission_classes = [permissions.AllowAny]
        return super(NewsViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "success": False,
                },
                status=403,
            )

    def update(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            data = request.data
            instance = NewsPost.objects.get(id=pk)
            serializer = self.get_serializer(instance, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "data": serializer.data,
                    },
                    status=200,
                )
        except NewsPost.DoesNotExist:
            raise NotFound(
                detail={"detail": "Id of news does not exist"}
            )

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            NewsPost.objects.get(id=pk).delete()
            return Response(
                {
                    "success": True,
                },
                status=200,
            )
        except NewsPost.DoesNotExist:
            raise NotFound(
                detail={"detail": "Id of news does not exist"}
            )

    @action(detail=False)
    def search(self, request):
        search = request.GET.get("key")
        queryset = self.get_queryset()
        if search:
            queryset = queryset.filter(Q(title__contains=str(
                search)) | Q(content__contains=str(
                    search)))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
