from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from umbrella.contracts.models import Contract, Node, Tag
from umbrella.core.serializers import CustomModelSerializer, CustomWritableNestedModelSerializer


class TagSerializer(CustomModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'type', 'contracts', 'group']

    def validate(self, attrs):
        tag_type = attrs.get('type') if 'type' in attrs.keys() else self.instance.type

        is_create_flow = not self.instance
        is_update_flow = self.instance
        tag_is_protected = tag_type != Tag.Types.OTHERS
        is_restricted_update_flow = not('contracts' in attrs.keys() and len(attrs) == 1)

        if tag_is_protected and is_create_flow:
            raise serializers.ValidationError("Only Others tag can be created")

        if tag_is_protected and is_update_flow and is_restricted_update_flow:
            raise serializers.ValidationError(f"{tag_type}' tag allows only contracts field to be updated")

        return attrs


class ContractSerializer(CustomWritableNestedModelSerializer):
    tags = TagSerializer(many=True, required=False)
    children = PrimaryKeyRelatedField(many=True, required=False, queryset=Contract.objects.all())
    created_by = serializers.StringRelatedField(read_only=True)
    groups = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'file_name', 'created_by', 'created_on', 'file_size', 'file_hash', 'status', 'parent',
                  'tags', 'groups', 'children']
        read_only_fields = ['groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].read_only = True


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
        fields = ['id', 'file_name', 'children', 'tasks', 'contracting_parties', 'starts', 'tags', 'contract_types',
                  'tasks', 'groups']

    def get_fields(self):
        fields = super(DocumentLibrarySerializer, self).get_fields()
        fields['children'] = DocumentLibrarySerializer(many=True)
        return fields


class ContractClauseProcessedWebhookSerializer(serializers.Serializer):
    aws_file_path = serializers.CharField()

    def validate_aws_file_path(self, value):
        if not value.endswith('.json'):
            raise serializers.ValidationError(f"File {value} should have .json extension.")

        return value
