import logging

from rest_framework import serializers

from contact.serializers import ContactSerializer
from .models import Appointment, AppointmentNotification, AppointmentNote, AppointmentDrivingTime

logger = logging.getLogger(__name__)


class AppointmentNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentNote
        fields = '__all__'


class AppointmentDrivingTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointmentDrivingTime
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    contact = ContactSerializer(read_only=True)
    notes = AppointmentNoteSerializer(many=True, required=False)
    driving_times = AppointmentDrivingTimeSerializer(many=True, required=False)

    def create(self, validated_data):
        notes = validated_data.pop('notes', [])
        appointment = super().create(validated_data)
        notes_list = []
        for note in notes:
            ans = AppointmentNoteSerializer(data=note)
            ans.is_valid(raise_exception=True)
            notes_list.append(ans.save())
        appointment.notes.set(notes_list)
        return appointment

    def update(self, instance, validated_data):
        notes = validated_data.pop('notes', [])
        super().update(instance, validated_data)
        for note in notes:
            instance_note, _ = instance.notes.get_or_create(type=note['type'])
            instance_note.note = note['note']
            instance_note.save()
        return instance

    def validate_notes(self, value):
        types_list = []
        for note in value:
            if note['type'] in types_list:
                raise serializers.ValidationError(
                    'every type is only allowed once')
            types_list.append(note['type'])
        return value

    def validate_type(self, value):
        if not value:
            raise serializers.ValidationError(
                'type must be an array of one or more string elements')
        return value

    def validate_organization_uuid(self, value):
        if value:
            request = self.context['request']
            user_org_uuid = request.session.get('jwt_organization_uuid')
            if user_org_uuid != str(value):
                raise serializers.ValidationError(
                    'The Organization cannot be different than user\'s '
                    'organization')
        return value

    class Meta:
        model = Appointment
        exclude = ('owner',)


class AppointmentHyperlinkField(serializers.HyperlinkedRelatedField):
    view_name = 'appointment-detail'
    queryset = Appointment.objects.all()
    lookup_field = 'uuid'


class AppointmentNotificationSerializer(serializers.HyperlinkedModelSerializer):  # noqa
    id = serializers.ReadOnlyField()
    sent_at = serializers.ReadOnlyField()
    appointment = AppointmentHyperlinkField()

    class Meta:
        model = AppointmentNotification
        fields = '__all__'
