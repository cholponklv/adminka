from rest_framework import serializers
from .models import Project, Bedroom, Characteristic, MasterPlan, Photo, PriceList, Type, TypePhoto, Design, PhotoDesign




class BedroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bedroom
        fields = '__all__'

class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'

class MasterPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterPlan
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'



class TypePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePhoto
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    photo = TypePhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Type
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['photo'] = TypePhotoSerializer(instance.photo.all(), many=True).data
        return representation

class PhotoDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoDesign
        fields = '__all__'

class DesignSerializer(serializers.ModelSerializer):
    photo = PhotoDesignSerializer(many=True, read_only=True)

    class Meta:
        model = Design
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['photo'] = PhotoDesignSerializer(instance.photo.all(), many=True).data
        return representation
    


class PriceListSerializer(serializers.ModelSerializer):
    design = DesignSerializer()
    type = TypeSerializer()

    class Meta:
        model = PriceList
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['design'] = DesignSerializer(instance.design).data
        representation['type'] = TypeSerializer(instance.project).data
        return representation

class ProjectSerializer(serializers.ModelSerializer):
    count_bedrooms = BedroomSerializer(many=True, read_only=True)
    characteristic = CharacteristicSerializer(many=True, read_only=True)
    master_plan = MasterPlanSerializer(many=True, read_only=True)
    photo = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['count_bedrooms'] = BedroomSerializer(instance.count_bedrooms.all(), many=True).data
        representation['characteristic'] = CharacteristicSerializer(instance.characteristic.all(), many=True).data
        representation['master_plan'] = MasterPlanSerializer(instance.master_plan.all(), many=True).data
        representation['photo'] = PhotoSerializer(instance.photo.all(), many=True).data
        return representation