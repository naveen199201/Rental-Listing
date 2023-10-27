from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics, viewsets
from django.views.generic import CreateView
from .models import Property, CustomUser, Applicant, TENANT, LANDLORD
from .serializers import PropertySerializer,ApplicantSerializer,CustomUserSerializer
from rest_auth.registration.views import RegisterView
from django.db.models import Q


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        custom_data = {"message": "registration succesfull", "status": "ok"}
        response.data.update(custom_data)
        data = request.data
        user = CustomUser.objects.get(email=data.get('email'))
        user.phone_number = data.get('phone_number')
        user.role = data.get('role')
        # user.email = data.get('email'))
        user.save()
        return response
    

# class UserListView(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = serializers.UserSerializer

class PropertyView(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset
        landlord = self.request.query_params.get('landlord', None)
        query = self.request.query_params.get('query', None)
        if landlord is not None:
            queryset = queryset.filter(landlord__email=landlord)
        if query is not None:
            queryset = queryset.filter(Q(address__icontains=query)| Q(description__icontains=query))
        return queryset

class ApplicantView(viewsets.ModelViewSet):
    queryset=Applicant.objects.all()
    serializer_class=ApplicantSerializer

    def get_queryset(self):  
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset
        property_id = self.request.query_params.get('property_id', None)
        title = self.request.query_params.get('title', None)
        if property_id is not None:
            queryset = queryset.filter(address__pk=property_id)
        if title is not None:
            queryset = queryset.filter(title__id=title)
        return queryset
    def perform_create(self, serializer):
        serializer.save()
    
class TenantView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(role=TENANT)
        return query_set

    def perform_create(self, serializer):
        serializer.save(role=TENANT)

class LandLordView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(role=LANDLORD)
        return query_set

    def perform_create(self, serializer):
        serializer.save(role=LANDLORD)

class GetSuggestionsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = request.data
        print(data)
        content = {'message':data.get('query')}
        return Response(content)