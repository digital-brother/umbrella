from rest_framework import serializers

from umbrella.contracts.models import Lease, Node
from umbrella.core.serializers import CustomModelSerializer


class GetAddFilePresignedUrlSerializer(CustomModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lease
        fields = ('id', 'file_name', 'file_size', 'file_hash', 'created_by')

    def validate(self, attrs):
        """
        Validate before call to AWS presigned url
        https://www.kye.id.au/posts/django-rest-framework-model-full-clean/
        """
        data = {**attrs, **{'modified_file_name': Lease.generate_modified_file_name(attrs['file_name'])}}
        instance = Lease(**data)
        instance.full_clean()
        return attrs


class LeaseSerializer(CustomModelSerializer):
    class Meta:
        model = Lease
        fields = ['id', 'file_name', 'created_by', 'created_on', 'file_size', 'status']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('type', 'content')


class NodeSerializer(CustomModelSerializer):
    clause = serializers.PrimaryKeyRelatedField(read_only=True)
    subcategories = SubCategorySerializer()

    class Meta:
        model = Node
        fields = ["id", "type", "clause", "lease", "content", "subcategories"]

# class CategorySerializer(serializers.ModelSerializer):
#     parentCategory = serializers.PrimaryKeyRelatedField()
#     subcategories = serializers.SubCategorySerializer()
#
#     class Meta:
#         model = Category
#         fields = ('parentCategory', 'name', 'description', 'subcategories')
