from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Project, Characteristic, MasterPlan, Photo, PriceList, Type, TypePhoto, Design, PhotoDesign,Archive
from .serializers import ProjectSerializer,  CharacteristicSerializer, MasterPlanSerializer, PhotoSerializer, PriceListSerializer, TypeSerializer, TypePhotoSerializer, DesignSerializer, PhotoDesignSerializer,DesignSerializer2
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction
from django.shortcuts import get_object_or_404


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        characteristic_data = request.data.pop('characteristic', [])  

        project_serializer = self.get_serializer(data=request.data)
        project_serializer.is_valid(raise_exception=True)
        self.perform_create(project_serializer)
        instance = project_serializer.instance
        for characteristic_id in characteristic_data:
            characteristic = Characteristic.objects.get(id=characteristic_id)
            instance.characteristic.add(characteristic)

        headers = self.get_success_headers(project_serializer.data)
        return Response(project_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'])
    def update_price_list(self, request, pk=None, price_list_pk=None):
        project = self.get_object()
        price_list = get_object_or_404(PriceList, project=project, pk=price_list_pk)
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
    def delete_price_list(self, request, pk=None, price_list_pk=None):
        try:
            project = self.get_object()
            price_list = PriceList.objects.get(project=project, pk=price_list_pk)
            price_list.delete()
            return Response({"message": "Price list deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except PriceList.DoesNotExist:
            return Response({"message": "Price list not found."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['post'])
    def copy_price_list(self, request, pk=None, price_list_pk=None):
        try:
            project = self.get_object()
            original_price_list = PriceList.objects.get(project=project, pk=price_list_pk)

            with transaction.atomic():
                copied_price_list = PriceList.objects.create(
                    no=original_price_list.no,
                    type=original_price_list.type,
                    status=original_price_list.status,
                    count_bedroom=original_price_list.count_bedroom,
                    land_area=original_price_list.land_area,
                    building_area=original_price_list.building_area,
                    villa=original_price_list.villa,
                    price=original_price_list.price,
                    design=original_price_list.design,
                    project=project
                )

            return Response({"message": "Price list copied successfully.", "copied_price_list_id": copied_price_list.id}, status=status.HTTP_201_CREATED)
        except PriceList.DoesNotExist:
            return Response({"message": "Price list not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def price_lists(self, request, pk=None):
        project = self.get_object()
        price_lists = PriceList.objects.filter(project=project)
        serializer = PriceListSerializer(price_lists, many=True)
        return Response(serializer.data)
     
    @action(detail=True, methods=['get'])
    def price_list_detail(self, request, pk=None, price_list_pk=None):
        project = self.get_object()
        price_list = PriceList.objects.filter(project=project, pk=price_list_pk).first()
        if not price_list:
            return Response({"message": "Price list not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PriceListSerializer(price_list)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def hide_price_list(self, request, pk=None, price_list_pk=None):
        try:
            project = self.get_object()
            price_list = PriceList.objects.get(project=project, pk=price_list_pk)
            if price_list.is_active:
                price_list.is_active = False
            else:
                price_list.is_active = True
            price_list.save()
            return Response({"message": "Price list status updated successfully."}, status=status.HTTP_200_OK)
        except PriceList.DoesNotExist:
            return Response({"message": "Price list not found."}, status=status.HTTP_404_NOT_FOUND)
        
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
    
    @action(detail=True, methods=['get'])
    def view_design_detail(self, request, pk=None, design_pk=None):
        project = self.get_object()
        design = get_object_or_404(Design, project=project, pk=design_pk)
        serializer = DesignSerializer(design)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_design(self, request, pk=None, design_pk=None):
        project = self.get_object()
        design = get_object_or_404(Design, project=project, pk=design_pk)
        serializer = DesignSerializer(design, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_design(self, request, pk=None, design_pk=None):
        project = self.get_object()
        design = get_object_or_404(Design, project=project, pk=design_pk)
        design.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def archive_project(self, request, pk=None):
        project = self.get_object()
        project.is_active = False
        project.save()
        archive = Archive.objects.create(project=project)
       

        return Response({'message': 'Project has been archived.'})

    @action(detail=True, methods=['post'])
    def restore_project(self, request, pk=None):
        project = self.get_object()
        project.is_active = True
        project.save()

        archive_instance = Archive.objects.get(project=project)
        archive_instance.delete()

        return Response({'message': 'Project has been restored and removed from the archive.'})



class CharacteristicViewSet(viewsets.ModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer

class MasterPlanViewSet(viewsets.ModelViewSet):
    queryset = MasterPlan.objects.all()
    serializer_class = MasterPlanSerializer

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class PriceListViewSet(viewsets.ModelViewSet):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer

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
