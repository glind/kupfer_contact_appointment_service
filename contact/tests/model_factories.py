import uuid

from factory import DjangoModelFactory, Iterator, PostGenerationMethodCall, LazyFunction, SubFactory
from django.contrib.auth.models import User

from ..models import Contact as ContactM, Type as TypeM


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User

    email = 'admin@example.com'
    username = 'admin'
    password = PostGenerationMethodCall('set_password', 'adm1n')

    is_superuser = True
    is_staff = True
    is_active = True


class Type(DjangoModelFactory):
    organization_uuid = LazyFunction(uuid.uuid4)

    class Meta:
        model = TypeM


class Contact(DjangoModelFactory):

    class Meta:
        model = ContactM

    core_user_uuid = uuid.uuid4()
    first_name = Iterator(['David', 'Nina'])
    last_name = Iterator(['Bowie', 'Simone'])
    title = Iterator(['mr', 'ms'])
    customer_type = Iterator(['customer', 'public'])
    company = Iterator(['RCA', 'Motown'])
    addresses = []
    emails = Iterator([
        [
            {'type': 'private', 'email': 'contact@bowie.co.uk'},
            {'type': 'office', 'email': 'bowie@label.co.uk'},
        ],
        [
            {'type': 'private', 'email': 'contact@ninasimone.com'},
            {'type': 'office', 'email': 'simone@label.com'},
        ],
    ])
    phones = []
    notes = Iterator(["Bowie's notes", "Nina's notes"])
    organization_uuid = str(uuid.uuid4())
    workflowlevel1_uuids = [str(uuid.uuid4())]

