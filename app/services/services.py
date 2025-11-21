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
    free_objects_model = model_object.investment_counterpart

    result = await session.execute(
        select(free_objects_model)
        .where(~free_objects_model.fully_invested)
        .order_by(free_objects_model.create_date)
    )

    free_objects = result.scalars().all()

    # --- GUARD CLAUSE: нет свободных объектов ---
    if not free_objects:
        return model_object

    model_remaining = model_object.full_amount - model_object.invested_amount

    for free_object in free_objects:
        free_remaining = free_object.full_amount - free_object.invested_amount

        # free < model → вложили объект полностью
        if free_remaining < model_remaining:
            model_object.invested_amount += free_remaining
            await closing_single_investment(free_object, session)
            model_remaining -= free_remaining
            continue

        # free == model → оба закрываются
        if free_remaining == model_remaining:
            await closing_single_investment(model_object, session)
            await closing_single_investment(free_object, session)
            break

        # free > model → закрывается model_object
        free_object.invested_amount += model_remaining
        await closing_single_investment(model_object, session)
        break

    await session.commit()
    await session.refresh(model_object)
    return model_object
