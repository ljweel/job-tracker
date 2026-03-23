from rest_framework import serializers
from .models import ResumeEvent


class ResumeEventSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = ResumeEvent
        fields = ['id', 'label', 'modified_date', 'pdf_file', 'pdf_url']
        extra_kwargs = {
            'pdf_file': {'write_only': True},
        }

    def get_pdf_url(self, obj):
        if obj.pdf_file:
            return obj.pdf_file.url
        return None
