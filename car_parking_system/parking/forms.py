from django import forms
from .models import Project, Tower, Floor, ParkingNumber

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']


class TowerForm(forms.ModelForm):
    class Meta:
        model = Tower
        fields = ['project', 'tower_name']

class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['tower', 'floor_name']

class ParkingNumberForm(forms.ModelForm):
    class Meta:
        model = ParkingNumber
        fields = ['floor', 'parking_number']
