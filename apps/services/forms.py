from django import forms
from .models import Service, PriceOption, CategoryDetail, Review

class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'category_detail']

    def __init__ (self, *args, **kwargs):
        super(CreateServiceForm, self).__init__(*args, **kwargs)
        self.fields['service_name'] = forms.CharField(max_length=100)
        self.fields['category_detail'] = forms.ModelChoiceField(queryset=CategoryDetail.objects.all())

class PriceOptionForm(forms.ModelForm):

    class Meta:
        model = PriceOption
        fields = ['price', 'price_option_name', 'description']
    
    def __init__ (self, *args, **kwargs):
        super(PriceOptionForm, self).__init__(*args, **kwargs)
        self.fields['price'] = forms.DecimalField()
        self.fields['price_option_name'] = forms.CharField(max_length=100)
        self.fields['description'] = forms.CharField(max_length=1000)
         
class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

    def __init__ (self, *args, **kwargs):
        super(CreateReviewForm, self).__init__(*args, **kwargs)
        self.fields['content'] = forms.CharField(max_length=1000)

class CreateReviewCommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

    def __init__ (self, *args, **kwargs):
        super(CreateReviewCommentForm, self).__init__(*args, **kwargs)
        self.fields['content'] = forms.CharField(max_length=1000)