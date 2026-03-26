import os
from rest_framework import serializers
from .models import ResumeEvent


class ResumeEventSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = ResumeEvent
        fields = ['id', 'doc_type', 'label', 'modified_date', 'pdf_file', 'pdf_url']
        extra_kwargs = {
            'pdf_file': {'write_only': True},
            'label': {'required': False, 'allow_blank': True},
        }

    def get_pdf_url(self, obj):
        if obj.pdf_file:
            return obj.pdf_file.url
        return None

    def validate(self, attrs):
        label = attrs.get('label', '')
        pdf_file = attrs.get('pdf_file')
        if not label and pdf_file:
            attrs['label'] = os.path.splitext(pdf_file.name)[0]
        elif not label:
            raise serializers.ValidationError({'label': '제목을 입력하거나 파일을 첨부해주세요.'})
        return attrs
