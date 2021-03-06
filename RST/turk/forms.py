from django.contrib.auth.models import User
from django import forms
from .models import Profile, Job, Bidder, FormToSuperUser, JobSubmission, ClientRateForm, ProtestWarning


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        #fields = ['name', 'age', 'email', 'money']
        fields = []
        #need to add uploading picture, resume etc...


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['job_title', 'job_description', 'bid_deadline', 'job_deadline']


class BidForm(forms.ModelForm):

    class Meta:
        model = Bidder
        fields = ['price']


class FormToSuperUser(forms.ModelForm):

    class Meta:
        model = FormToSuperUser
        fields = ['reason', 'writing']


class JobSubmissionForm(forms.ModelForm):

    class Meta:
        model = JobSubmission
        fields = ['submission', 'rating', 'reason']


class ClientRateForm(forms.ModelForm):

    class Meta:
        model = ClientRateForm
        fields = ['rating', 'reason']


class ProtestWarningForm(forms.ModelForm):

    class Meta:
        model = ProtestWarning
        fields = ['reason']

