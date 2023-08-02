from django import forms
# from .views import *

# 클라이언트 화면에 입력 폼을 만들어주기 위해 생성함
# 사용자 즉 클라이언트가 입력한 데이터에 대한 전처리 담당하게 하려고 생성

class AddMenuFrom(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)  # 불린필드 쓸 때 required=False 해야
#     options = forms.ModelMultipleChoiceField(
#         queryset=MenuOption.objects.all(),
#         widget=forms.CheckboxSelectMultiple(),
#         required=False
#     )