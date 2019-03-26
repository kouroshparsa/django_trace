from django.forms import ModelForm, SelectMultiple, TextInput, Textarea,\
    CheckboxSelectMultiple, Select, NumberInput, DateInput

class ConditionForm(ModelForm):
    class Meta:
        widgets = {
            'implications': CheckboxSelectMultiple(),
        }
