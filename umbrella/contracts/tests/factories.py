import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from umbrella.contracts.models import Contract, Clause, KDP, Tag, Node
from umbrella.tasks.models import Task
from umbrella.users.tests.factories import UserFactory


class ContractFactory(DjangoModelFactory):
    file_name = factory.Sequence(lambda n: f"contract_{n}.pdf")
    created_by = factory.SubFactory(UserFactory)
    file_size = 1024
    file_hash = factory.Sequence(lambda n: f"file_hash_{n}")
    modified_file_name = factory.Sequence(lambda n: f"modified_file_name_{n}")

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

    @factory.post_generation
    def clauses(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of tags were passed in, use them
            for extracted_clause in extracted:
                self.clauses.add(extracted_clause)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of tags were passed in, use them
            for extracted_tag in extracted:
                self.tags.add(extracted_tag)


@register
class TermClauseFactory(DjangoModelFactory):
    type = "term"
    contract = factory.SubFactory(ContractFactory)

    class Meta:
        model = Clause


@register
class TaskFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f"task_{n}")
    contract = factory.SubFactory(ContractFactory)

    class Meta:
        model = Task


@register
class StartKDPFactory(DjangoModelFactory):
    type = 'start'
    clause = factory.SubFactory(TermClauseFactory)
    contract = factory.LazyAttribute(lambda kdp: kdp.clause.contract)

    class Meta:
        model = KDP


class TagFactory(DjangoModelFactory):
    name = 'test_tag'
    type = Tag.TagTypes.OTHERS

    class Meta:
        model = Tag


class ContractingPartyFactory(DjangoModelFactory):
    type = "contractingParties"

    class Meta:
        model = Node
