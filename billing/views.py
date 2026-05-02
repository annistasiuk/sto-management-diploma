from django.http import HttpResponse
from .utils import render_to_pdf
from repairs.models import Repair

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.contrib import messages


def generate_invoice_pdf_view(request, repair_id):
    try:
        repair = Repair.objects.get(id=repair_id)
    except Repair.DoesNotExist:
        messages.error(request, 'Ремонт не знайдено.')
        return HttpResponse("Ремонт не знайдено", status=404)

    context = {
        'repair': repair,
        'total_cost': 1500.00
    }

    pdf = render_to_pdf('billing/invoice_template.html', context)

    if not pdf:
        messages.error(request, 'Помилка під час генерації PDF.')
        return HttpResponse("Помилка під час генерації PDF", status=500)

    pdf['Content-Disposition'] = f'attachment; filename="invoice_{repair.id}.pdf"'

    return pdf


def send_invoice_email_view(request, repair_id):
    try:
        repair = Repair.objects.get(id=repair_id)
    except Repair.DoesNotExist:
        messages.error(request, 'Ремонт не знайдено.')
        return redirect('repair_list')

    context = {'repair': repair, 'total_cost': 1500.00}

    template = get_template('billing/invoice_template.html')
    html = template.render(context)
    result = BytesIO()

    pisa_status = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if pisa_status.err:
        messages.error(request, 'Помилка при створенні PDF для email.')
        return redirect('repair_list')

    pdf_data = result.getvalue()

    subject = f"Рахунок за ремонт авто {repair.car.make} {repair.car.model_name}"
    body = "Доброго дня! У додатку ваш рахунок за ремонт."

    to_email = 'test@example.com'

    email = EmailMessage(subject, body, from_email='sto@example.com', to=[to_email])

    email.attach(f'invoice_{repair.id}.pdf', pdf_data, 'application/pdf')

    try:
        email.send()
        messages.success(request, f'Рахунок для {repair.car} успішно надіслано!')
    except Exception as e:
        messages.error(request, f'Помилка під час надсилання email: {e}')

    return redirect('repair_list')