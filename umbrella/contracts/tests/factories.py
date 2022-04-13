import factory
from factory.django import DjangoModelFactory

from umbrella.contracts.models import Contract, Node
from umbrella.users.tests.factories import UserFactory


class ContractFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    file_size = 1024

    class Meta:
        model = Contract

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for extracted_group in extracted:
                self.groups.add(extracted_group)


class NodeFactory(DjangoModelFactory):
    type = "term"
    contract = factory.SubFactory(ContractFactory)

    class Meta:
        model = Node
