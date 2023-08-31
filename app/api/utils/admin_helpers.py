from wtforms.validators import ValidationError


def validate_email(form, field):
    if '@' not in field.data:
        raise ValidationError('電子郵件格式錯誤')