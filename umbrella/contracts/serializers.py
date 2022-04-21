from rest_framework import serializers

from umbrella.contracts.models import Contract, Node, Tags
from umbrella.core.serializers import CustomModelSerializer

class ContractCreateSerializer(CustomModelSerializer):
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


class ClauseSerializer(CustomModelSerializer):
    class Meta:
        model = Node
        fields = ("id", "type", "contract", "content")


class KDPClauseSerializer(CustomModelSerializer):
    clause = ClauseSerializer()

    class Meta:
        model = Node
        fields = ["id", "type", "content", "clause"]


class TagsSerializer(CustomModelSerializer):
    class Meta:
        model = Tags
        fields = ['name', 'tag_group']


class DocumentLibrarySerializer(CustomModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    starts = KDPClauseSerializer(many=True, read_only=True)
    contract_types = KDPClauseSerializer(many=True, read_only=True)
    contract_parties = KDPClauseSerializer(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = ['file_name', 'children', 'tasks', 'contract_parties', 'starts', 'tags', 'contract_types', 'tasks']

    def get_fields(self):
        fields = super(DocumentLibrarySerializer, self).get_fields()
        fields['children'] = DocumentLibrarySerializer(many=True)
        return fields

