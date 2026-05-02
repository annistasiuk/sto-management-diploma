from django import forms
from .models import Repair
from masters.models import Master


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = [
            'car',
            'problem_description',
            'work_description',
            'status',
            'master',
            'planned_end_date',
            'end_date',
            'labor_cost',
            'parts_cost',
            'notes'
        ]

        widgets = {
            'car': forms.Select(attrs={'class': 'form-input'}),
            'problem_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'work_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'master': forms.Select(attrs={'class': 'form-input'}),
            'planned_end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'labor_cost': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'parts_cost': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }


class NewRepairRequestForm(forms.Form):
    client_full_name = forms.CharField(
        label='ПІБ клієнта',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Наприклад: Коваленко Олександр Петрович'
        })
    )

    client_phone = forms.CharField(
        label='Телефон клієнта',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+380...'
        })
    )

    client_email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'email@gmail.com'
        })
    )

    client_address = forms.CharField(
        label='Адреса',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Адреса клієнта'
        })
    )

    car_make = forms.CharField(
        label='Марка авто',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'BMW, Audi, Toyota'
        })
    )

    car_model = forms.CharField(
        label='Модель авто',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'X5, A6, Camry'
        })
    )

    license_plate = forms.CharField(
        label='Держномер',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'KA 1234 BT',
            'style': 'text-transform: uppercase;'
        })
    )

    vin = forms.CharField(
        label='VIN-код',
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '17 символів VIN',
            'maxlength': '17',
            'style': 'text-transform: uppercase;'
        })
    )

    year = forms.IntegerField(
        label='Рік випуску',
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': '2020'
        })
    )

    color = forms.CharField(
        label='Колір',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Чорний'
        })
    )

    main_image = forms.ImageField(
        label='Фото автомобіля',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-input',
            'accept': 'image/*'
        })
    )

    problem_description = forms.CharField(
        label='Опис несправності',
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 4,
            'placeholder': 'Опишіть проблему автомобіля'
        })
    )

    status = forms.ChoiceField(
        label='Статус ремонту',
        choices=Repair.Status.choices,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    master = forms.ModelChoiceField(
        label='Майстер',
        queryset=Master.objects.filter(is_active=True),
        required=False,
        empty_label='Не призначено',
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    labor_cost = forms.DecimalField(
        label='Вартість робіт',
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.01',
            'min': '0'
        })
    )

    parts_cost = forms.DecimalField(
        label='Вартість запчастин',
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'step': '0.01',
            'min': '0'
        })
    )


class QuickRepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = [
            'problem_description',
            'status',
            'master',
            'planned_end_date',
            'labor_cost',
            'parts_cost',
            'notes'
        ]

        widgets = {
            'problem_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'master': forms.Select(attrs={'class': 'form-input'}),
            'planned_end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'labor_cost': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'parts_cost': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }