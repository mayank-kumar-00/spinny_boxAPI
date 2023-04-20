from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .keys import *
from .models import Box
from .serializers import BoxSerializer, TokenObtainPairSerializer, RefreshTokenSerializer
from .utils import validate_data

class TokenObtainPairViewset(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RefreshTokenViewset(TokenRefreshView):
    serializer_class = RefreshTokenSerializer

class BoxView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = BoxSerializer

    def get(self, request):
        req_data = request.GET.copy()
        user = request.user
        all_data = req_data.get('all_data')
        boxs = Box.objects.filter(is_deleted=False)
        if not all_data:
            boxs = boxs.filter(user=user)
        data = self.serializer_class(boxs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        new_box = Box(user=user, updated_by=user, **data)
        result, msg, resp_status = validate_data(user, new_box, data)
        if not result:
            return Response({'message':msg}, status=resp_status)
        new_box.save()
        data = self.serializer_class(new_box).data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data['updated_by'] = user
        id = data.pop('id')
        box = Box.objects.filter(id=id)
        if not box.exists():
            return Response({'message':'Invalid Id'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        result, msg, resp_status = validate_data(user, box.first(), data)
        if not result:
            return Response({'message':msg}, status=resp_status)
        box.update(**data)
        data = self.serializer_class(box.first()).data
        return Response(data, status=status.HTTP_200_OK)
    
    
    def delete(self, request):
        user = request.user
        data = request.data.copy()
        id = data.pop('id')
        box = Box.objects.filter(id=id)
        if not box.exists():
            return Response({'message':'Invalid Id'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        data['updated_by'] = user
        data['is_deleted'] = True
        box.update(**data)
        return Response(status=status.HTTP_200_OK)