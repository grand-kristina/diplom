from celery import shared_task


@shared_task
def validation_cart_number(number):
    if int(number) % 2 == 0 and len(number) <= 8 and not number.endswith("0"):
        return True
    else:
        return False
