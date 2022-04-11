from rest_framework import serializers

from umbrella.contracts.models import Contract, Node
from umbrella.core.serializers import CustomModelSerializer
from umbrella.users.auth import User


class GetAddFilePresignedUrlSerializer(CustomModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contract
        fields = ('id', 'file_name', 'file_size', 'file_hash', 'created_by')

    def validate(self, attrs):
        """
        Validate before call to AWS presigned url
        https://www.kye.id.au/posts/django-rest-framework-model-full-clean/
        """
        data = {**attrs, **{'modified_file_name': Contract.generate_modified_file_name(attrs['file_name']),
                           'groups': Contract.add_user_group(attrs['created_by'])}}
        instance = Contract(**data)
        print(instance, "instance_data")
        instance.full_clean()

        return attrs


class ContractSerializer(CustomModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'file_name', 'created_by', 'created_on', 'file_size', 'status']


class ClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("id", "type", "contract", "content")


class KDPSerializer(CustomModelSerializer):
    clause = ClauseSerializer()

    class Meta:
        model = Node
        fields = ["id", "type", "content", "clause"]


class NodeSerializers(CustomModelSerializer):
    class Meta:
        model = Node
        fields = ['content', 'type']


class DocumentLibrarySerializer(serializers.ModelSerializer):
    data_for_document_library = NodeSerializers(many=True, read_only=True)
    contracts_task_statistic = serializers.CharField()
    task_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = ['file_name', 'task_set', 'data_for_document_library', 'contracts_task_statistic']