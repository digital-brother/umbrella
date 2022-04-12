from rest_framework import serializers

from umbrella.contracts.models import Contract, Node, Tags
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
        data = {**attrs, **{'modified_file_name': Contract.generate_modified_file_name(attrs['file_name'])}}
        instance = Contract(**data)
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


class TagsSerializers(CustomModelSerializer):
    class Meta:
        model = Tags
        fields = ['name', 'tag_group']


class ChildDocumentSerializer(CustomModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='task_set')
    tags = TagsSerializers(many=True, read_only=True, source='tags_set')
    contracting_start = NodeSerializers(many=True, read_only=True)
    contracts_type = NodeSerializers(many=True, read_only=True)
    contracting_parties = NodeSerializers(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = ['file_name', 'tasks', 'contracting_parties', 'contracting_start', 'tags',
                  'contracts_type']


class DocumentLibrarySerializer(CustomModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='task_set')
    get_child_contracts = ChildDocumentSerializer(many=True, read_only=True)
    tags = TagsSerializers(many=True, read_only=True, source='tags_set')
    contracting_start = NodeSerializers(many=True, read_only=True)
    contracts_type = NodeSerializers(many=True, read_only=True)
    contracting_parties = NodeSerializers(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = ['file_name', 'get_child_contracts', 'tasks', 'contracting_parties', 'contracting_start', 'tags', 'contracts_type']


class UpdateParentSerializer(CustomModelSerializer):

    class Meta:
        model = Contract
        fields = ['parent']


