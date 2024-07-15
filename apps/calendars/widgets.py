from django.forms import widgets


class CustomSelect(widgets.Select):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs, choices)
        self.option_labels = {
            "업무": "primary",
            "개인": "danger",
            "가족": "warning",
            "휴일": "success",
            "기타": "info",
        }

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        data_label = self.option_labels.get(label, "")
        if data_label:
            option["attrs"]["data-label"] = data_label
        if label == "업무":  # 기본 선택 옵션 설정
            option["attrs"]["selected"] = "selected"
        return option
