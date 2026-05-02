from django import forms
from .models import Car


class CarForm(forms.ModelForm):
    owner_phone = forms.CharField(
        label='Телефон власника',
        required=False
    )

    class Meta:
        model = Car
        fields = [
            'make',
            'model_name',
            'license_plate',
            'vin',
            'owner_name',
            'year',
            'color',
            'mileage',
            'engine_volume',
            'description',
            'main_image'
        ]

        labels = {
            'make': 'Марка',
            'model_name': 'Модель',
            'license_plate': 'Держномер',
            'vin': 'VIN-код',
            'owner_name': 'Власник',
            'year': 'Рік випуску',
            'color': 'Колір',
            'mileage': 'Пробіг',
            'engine_volume': 'Обʼєм двигуна',
            'description': 'Опис',
            'main_image': 'Фото',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.owner:
            self.fields['owner_phone'].initial = self.instance.owner.phone
