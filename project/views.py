from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Project, Bedroom, Characteristic, MasterPlan, Photo, PriceList, Type, TypePhoto, Design, PhotoDesign
from .serializers import ProjectSerializer, BedroomSerializer, CharacteristicSerializer, MasterPlanSerializer, PhotoSerializer, PriceListSerializer, TypeSerializer, TypePhotoSerializer, DesignSerializer, PhotoDesignSerializer,DesignSerializer2
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        count_bedrooms_data = request.data.pop('count_bedrooms', [])  
        characteristic_data = request.data.pop('characteristic', [])  

        project_serializer = self.get_serializer(data=request.data)
        project_serializer.is_valid(raise_exception=True)
        self.perform_create(project_serializer)

        
        instance = project_serializer.instance
        for count in count_bedrooms_data:
            bedroom, created = Bedroom.objects.get_or_create(count=count)
            instance.count_bedrooms.add(bedroom)

        
        for characteristic_id in characteristic_data:
            characteristic = Characteristic.objects.get(id=characteristic_id)
            instance.characteristic.add(characteristic)

        headers = self.get_success_headers(project_serializer.data)
        return Response(project_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'])
    def update_price_list(self, request, pk=None):
        project = self.get_object()
        price_list = PriceList.objects.get(project=project)
        serializer = PriceListSerializer(price_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_price_list(self, request, pk=None):
        project = self.get_object()
        serializer = PriceListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_price_list(self, request, pk=None):
        project = self.get_object()
        price_list = PriceList.objects.get(project=project)
        price_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def price_list(self, request, pk=None):
        project = self.get_object()
        price_lists = PriceList.objects.filter(project=project)
        serializer = PriceListSerializer(price_lists, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

    @action(detail=True, methods=['post'])
    def create_design(self, request, pk=None):
        project = self.get_object()
        data = request.data.copy()
        data['project'] = project.id
        serializer = DesignSerializer2(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view_design(self, request, pk=None):
        project = self.get_object()
        designs = project.design_set.all()
        serializer = DesignSerializer(designs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_design(self, request, pk=None):
        project = self.get_object()
        design_id = request.data.get('design_id')
        data = request.data.copy()
        data['project'] = project.id
        design = project.design_set.get(id=design_id)
        serializer = DesignSerializer(design, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_design(self, request, pk=None):
        project = self.get_object()
        design_id = request.data.get('design_id')
        design = project.design_set.get(id=design_id)
        design.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BedroomViewSet(viewsets.ModelViewSet):
    queryset = Bedroom.objects.all()
    serializer_class = BedroomSerializer

class CharacteristicViewSet(viewsets.ModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer

class MasterPlanViewSet(viewsets.ModelViewSet):
    queryset = MasterPlan.objects.all()
    serializer_class = MasterPlanSerializer

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer



class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class TypePhotoViewSet(viewsets.ModelViewSet):
    queryset = TypePhoto.objects.all()
    serializer_class = TypePhotoSerializer

class DesignViewSet(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer

class PhotoDesignViewSet(viewsets.ModelViewSet):
    queryset = PhotoDesign.objects.all()
    serializer_class = PhotoDesignSerializer
