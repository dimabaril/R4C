from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def notify_customer_robot_available(sender, instance, created, **kwargs):
    if created:
        orders = Order.objects.filter(robot_serial=instance.serial)
        for order in orders:
            send_mail(
                subject="Ваш робот теперь в наличии",
                message=f"Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}. "
                f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.customer.email],
            )
            # # if you are too lazy to set up mail, you can print it
            # print(
            #     "subject: Ваш робот теперь в наличии\n"
            #     "message: Добрый день!\n"
            #     f"Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\n"
            #     "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.\n"
            #     "from_email: dimabaril@mail.ru\n"
            #     f"recipient_list=[{order.customer.email}]\n"
            # )
