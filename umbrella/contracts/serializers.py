import traceback

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from umbrella.contracts.models import Lease


class BusinessLogicModelSerializer(serializers.ModelSerializer):
    """
    Updated serializer create to call business logic
    https://www.kye.id.au/posts/django-rest-framework-model-full-clean/
    """

    def perform_create_business_logic(self, **validated_data):
        msg = 'Derived class should self.implement perform_create_business_logic() method'
        raise NotImplementedError(msg)

    # Default `create` and `update` behavior...
    def create(self, validated_data):
        """
        Updated serializer create to call business logic
        https://www.kye.id.au/posts/django-rest-framework-model-full-clean/

        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

            return ExampleModel.objects.create(**validated_data)

        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:

            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance

        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            # instance = ModelClass._default_manager.create(**validated_data)
            instance = self.perform_create_budiness_logic(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance


class GetAddFilePresignedUrlSerializer(BusinessLogicModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lease
        fields = ('file_name', 'file_size', 'file_hash', 'created_by')

    def perform_create_budiness_logic(self, **validated_data):
        return Lease.objects.create_lease(**validated_data)

    def validate(self, attrs):
        """
        Validate before call to AWS presigned url
        https://www.kye.id.au/posts/django-rest-framework-model-full-clean/
        """
        data = {**attrs, **{'modified_file_name': Lease.generate_modified_file_name(attrs['file_name'])}}
        instance = Lease(**data)
        instance.full_clean()
        return attrs
