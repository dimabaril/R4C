import datetime

from openpyxl import Workbook

from robots.models import Robot


def generate_robot_production_summary(
    from_time: datetime.datetime,
    to_time: datetime.datetime,
) -> Workbook:
    workbook = Workbook()

    all_models = Robot.objects.values_list("model", flat=True).distinct()

    for model in all_models:
        worksheet = workbook.create_sheet(title=model)
        worksheet.append(["Модель", "Версия", "Количество за неделю"])

        all_versions = (
            Robot.objects.filter(model=model)
            .values_list("version", flat=True)
            .distinct()
        )

        for version in all_versions:
            count = Robot.objects.filter(
                model=model,
                version=version,
                created__gte=from_time,
                created__lte=to_time,
            ).count()
            worksheet.append([model, version, count])

    # Delete default empty sheet
    if "Sheet" in workbook.sheetnames:
        workbook.remove(workbook["Sheet"])

    return workbook
