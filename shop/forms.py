from django import forms

from shop.models import Comment, Customer


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['product', 'created_date', 'updated_date']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['created_date', 'updated_date', ]
