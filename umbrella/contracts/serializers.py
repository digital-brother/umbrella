from rest_framework import serializers

from umbrella.contracts.models import Contract, Node, Tag
from umbrella.core.serializers import CustomModelSerializer, CustomWritableNestedModelSerializer


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


class TagSerializer(CustomModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'type', 'contracts', 'group']

    def validate(self, attrs):
        contracts = attrs.get('contracts', None)
        type = attrs.get('type', None)
        if self.instance and self.instance.type != Tag.TagTypes.OTHERS:
            if not contracts or len(attrs) != 1:
                raise serializers.ValidationError("Only Others tag type is allowed for edit")
        if not self.instance and type != Tag.TagTypes.OTHERS:
            raise serializers.ValidationError("Only Others tag can be created")
        return attrs


class ContractSerializer(CustomWritableNestedModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Contract
        fields = ['id', 'file_name', 'created_by', 'created_on', 'file_size', 'file_hash', 'status', 'parent',
                  'tags', 'groups', 'children']
        read_only_fields = ['groups']


class ClauseSerializer(CustomModelSerializer):
    class Meta:
        model = Node
        fields = ("id", "type", "contract", "content")


class KDPClauseSerializer(CustomModelSerializer):
    clause = ClauseSerializer()

    class Meta:
        model = Node
        fields = ["id", "type", "content", "clause"]


class DocumentLibrarySerializer(CustomModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    starts = KDPClauseSerializer(many=True, read_only=True)
    contract_types = KDPClauseSerializer(many=True, read_only=True)
    contracting_parties = KDPClauseSerializer(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = ['file_name', 'children', 'tasks', 'contracting_parties', 'starts', 'tags', 'contract_types', 'tasks', 'groups']

    def get_fields(self):
        fields = super(DocumentLibrarySerializer, self).get_fields()
        fields['children'] = DocumentLibrarySerializer(many=True)
        return fields
