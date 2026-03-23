from rest_framework import serializers
from .models import Company, CompanyStage


class CompanyStageSerializer(serializers.ModelSerializer):
    resume_label = serializers.CharField(source='resume.label', read_only=True, default=None)
    resume_pdf_url = serializers.SerializerMethodField()
    stage = serializers.JSONField()

    class Meta:
        model = CompanyStage
        fields = ['id', 'stage', 'method', 'date', 'result', 'memo', 'resume', 'resume_label', 'resume_pdf_url']

    def get_resume_pdf_url(self, obj):
        if obj.resume and obj.resume.pdf_file:
            return obj.resume.pdf_file.url
        return None

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
