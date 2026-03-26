from rest_framework import serializers
from .models import Company, CompanyStage


class DocumentInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    doc_type = serializers.CharField()
    label = serializers.CharField()
    pdf_url = serializers.SerializerMethodField()

    def get_pdf_url(self, obj):
        if obj.pdf_file:
            return obj.pdf_file.url
        return None


class CompanyStageSerializer(serializers.ModelSerializer):
    documents_detail = DocumentInfoSerializer(source='documents', many=True, read_only=True)
    document_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False, default=list,
    )
    stage = serializers.JSONField()

    class Meta:
        model = CompanyStage
        fields = ['id', 'stage', 'method', 'date', 'result', 'memo',
                  'documents_detail', 'document_ids']

    @staticmethod
    def _expand_stage(raw):
        if isinstance(raw, list):
            result = []
            for item in raw:
                result.extend(CompanyStageSerializer._expand_stage(item))
            return result

        if isinstance(raw, str):
            trimmed = raw.strip()
            if not trimmed:
                return []
            try:
                parsed = serializers.JSONField().to_internal_value(trimmed)
                if isinstance(parsed, list):
                    result = []
                    for item in parsed:
                        result.extend(CompanyStageSerializer._expand_stage(item))
                    return result
            except Exception:
                pass
            return [raw]

        if raw is None:
            return []

        return [str(raw)]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['stage'] = self._expand_stage(instance.stage)
        return data

    def validate_stage(self, value):
        value = self._expand_stage(value)

        if len(value) == 0:
            raise serializers.ValidationError('형태는 1개 이상 선택해야 합니다.')

        valid_values = {choice for choice, _ in CompanyStage.Stage.choices}
        invalid_values = [item for item in value if item not in valid_values]
        if invalid_values:
            raise serializers.ValidationError(f'유효하지 않은 형태입니다: {", ".join(invalid_values)}')

        return value

    def validate_document_ids(self, value):
        if not value:
            return value
        from resumes.models import ResumeEvent
        docs = list(ResumeEvent.objects.filter(id__in=value))
        if len(docs) != len(value):
            raise serializers.ValidationError('존재하지 않는 서류가 포함되어 있습니다.')
        doc_types = [d.doc_type for d in docs]
        if len(doc_types) != len(set(doc_types)):
            raise serializers.ValidationError('같은 종류의 서류를 중복 선택할 수 없습니다.')
        return value

    def create(self, validated_data):
        document_ids = validated_data.pop('document_ids', [])
        instance = super().create(validated_data)
        if document_ids:
            instance.documents.set(document_ids)
        return instance

    def update(self, instance, validated_data):
        document_ids = validated_data.pop('document_ids', [])
        instance = super().update(instance, validated_data)
        instance.documents.set(document_ids)
        return instance


class CompanyListSerializer(serializers.ModelSerializer):
    first_stage_date = serializers.DateField(read_only=True, allow_null=True)
    last_stage_date = serializers.DateField(read_only=True, allow_null=True)
    status = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'position', 'source', 'job_url',
                  'status', 'memo', 'created_at', 'updated_at', 'first_stage_date', 'last_stage_date']
        read_only_fields = ['created_at', 'updated_at']


class CompanyDetailSerializer(serializers.ModelSerializer):
    stages = CompanyStageSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'position', 'source', 'job_url',
                  'status', 'memo', 'created_at', 'updated_at', 'stages']
        read_only_fields = ['created_at', 'updated_at']
