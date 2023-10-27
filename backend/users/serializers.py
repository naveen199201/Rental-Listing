from rest_framework import serializers,generics
from . import models
import logging
logger = logging.getLogger("test")

class PropertySerializer(serializers.ModelSerializer):
    email=serializers.CharField(source='landlord.email')
    class Meta:
        model = models.Property
        fields = ('email', 'address', 'description', 'latitude', 'longitude', 'image','id','title')
     
    def create(self,validated_data):
        try:
            print(validated_data)
            landlord_object = models.CustomUser.objects.get(email=validated_data['landlord']['email'], role=models.LANDLORD)
        except Exception as e:
            logger.exception("Unable to find landlord with the email")
            raise Exception
        newproperty = models.Property.objects.create(landlord=landlord_object,address=validated_data['address'],description=validated_data['description'],latitude=validated_data['latitude'],longitude=validated_data['longitude'],image=validated_data['image'])
        # applicant = super().create(validated_data)
        newproperty.save()
        # logger.info("Created applicant with email {} and propery {}".format(tenant_object, property_object))
        return newproperty
    
    def delete(self, instance):
        instance.delete()
        
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model=models.CustomUser
        fields=('name','email','password','phone_number','role','username')
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user

class ApplicantSerializer(serializers.ModelSerializer):
    # tenant = CustomUserSerializer(many=False)
    email = serializers.CharField(source='tenant.email')
    phone_number = serializers.CharField(source='tenant.phone_number',read_only=True)
    username=serializers.CharField(source='tenant.username',read_only=True)
    class Meta:
        model=models.Applicant
        fields=['email','duration','address','phone_number','username']
    
    def create(self, validated_data):
        try:
            print(validated_data)
            tenant_object = models.CustomUser.objects.get(email=validated_data['tenant']['email'], role=models.TENANT)
        except Exception as e:
            logger.exception("Unable to find tenant with the email")
            raise Exception
        applicant = models.Applicant.objects.create(tenant=tenant_object, address=validated_data['address'], duration=validated_data['duration'])
        # applicant = super().create(validated_data)
        applicant.save()
        # logger.info("Created applicant with email {} and propery {}".format(tenant_object, property_object))
        return applicant

# class UserChangeView(generics.UpdateAPIView):
#     queryset = models.CustomUser.objects.all()
#     serializer_class = UserSerializer