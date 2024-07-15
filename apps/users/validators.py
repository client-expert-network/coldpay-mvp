from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password.replace(" ", "")) < 8:
            raise ValidationError("비밀번호는 공백을 제외하고 8자 이상이어야 합니다.")
        
        if len(password) > 32:
            raise ValidationError("비밀번호는 32자 이하여야 합니다.")
        
        categories = 0
        if re.search(r'[A-Za-z]', password):
            categories += 1
        if re.search(r'\d', password):
            categories += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            categories += 1
        
        if categories < 2:
            raise ValidationError("비밀번호는 영문, 숫자, 특수문자 중 2가지 이상을 포함해야 합니다.")
        
        if re.search(r'(.)\1\1', password):
            raise ValidationError("비밀번호에 3번 연속으로 반복되는 문자가 있으면 안 됩니다.")