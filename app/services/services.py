from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def closing_project(
        project: CharityProject,
        session: AsyncSession
):
    """
    Помечает проект как полностью инвестированный
    и устанавливает дату окончания приема инвестиций
    """
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
        await session.commit()
        await session.refresh(project)
    return project


async def closing_single_investment(
        object,
        session: AsyncSession):
    """
    Помечает один взнос как полностью инвестированный.
    """
    object.invested_amount = object.full_amount
    object.fully_invested = True
    object.close_date = datetime.now()
    session.refresh(object)


async def investment_process(
        model_object,
        session: AsyncSession
):
    """
    Процесс распределения инвестиций между пожертвованиями и
    благотворительными проектами.
    """
    if isinstance(model_object, Donation):
        free_objects_model = CharityProject
    else:
        free_objects_model = Donation
    free_objects = await session.execute(
        select(free_objects_model).where(
            ~free_objects_model.fully_invested
        ).order_by(free_objects_model.create_date)
    )
    if free_objects:
        for free_object in free_objects.scalars().all():
            if (
                (free_object.full_amount - free_object.invested_amount
                 ) < (model_object.full_amount - model_object.invested_amount)
            ):
                model_object.invested_amount += ((free_object.full_amount -
                                                  free_object.invested_amount))
                await closing_single_investment(free_object, session)
                continue
            if (
                (free_object.full_amount - free_object.invested_amount
                 ) == (model_object.full_amount - model_object.invested_amount)
            ):
                await closing_single_investment(model_object, session)
                await closing_single_investment(free_object, session)
                break
            free_object.invested_amount += ((model_object.full_amount -
                                             model_object.invested_amount))
            await closing_single_investment(model_object, session)
            break
        await session.commit()
        await session.refresh(model_object)
        return model_object
