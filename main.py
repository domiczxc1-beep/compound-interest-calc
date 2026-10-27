import argparse
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class YearlyReport:
    year: int
    deposited_this_year: float
    interest_this_year: float
    total_interest: float
    end_balance: float


def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    years: int,
    monthly_deposit: float = 0.0,
) -> List[YearlyReport]:
    """
    Рассчитывает сложный процент с ежемесячным капитализацией и взносами.
    """
    monthly_rate = (annual_rate / 100) / 12
    current_balance = principal
    accumulated_interest = 0.0
    schedule: List[YearlyReport] = []

    for year in range(1, years + 1):
        yearly_deposit = 0.0
        yearly_interest = 0.0

        for _ in range(12):
            # Начисление процентов за текущий месяц
            month_interest = current_balance * monthly_rate
            yearly_interest += month_interest
            accumulated_interest += month_interest

            # Пополнение и обновление баланса
            current_balance += month_interest + monthly_deposit
            yearly_deposit += monthly_deposit

        schedule.append(
            YearlyReport(
                year=year,
                deposited_this_year=yearly_deposit,
                interest_this_year=yearly_interest,
                total_interest=accumulated_interest,
                end_balance=current_balance,
            )
        )

    return schedule


def render_table(
    principal: float,
    annual_rate: float,
    years: int,
    monthly_deposit: float,
    schedule: List[YearlyReport],
) -> None:
    """Выводит красиво отформатированный отчет в консоль."""
    total_user_deposits = principal + sum(r.deposited_this_year for r in schedule)
    final_balance = schedule[-1].end_balance if schedule else principal
    total_interest = schedule[-1].total_interest if schedule else 0.0

    divider = "─" * 68

    print("\n" + "═" * 68)
    print("         ФИНАНСОВЫЙ РАСЧЕТ: СЛОЖНЫЙ ПРОЦЕНТ И НАКОПЛЕНИЯ")
    print("═" * 68)
    print(f" Начальный капитал:       {principal:>15,.2f} ₽")
    print(f" Ежемесячное пополнение:  {monthly_deposit:>15,.2f} ₽")
    print(f" Годовая ставка:          {annual_rate:>15.2f} %")
    print(f" Срок инвестирования:     {years:>15d} лет")
    print(divider)

    header = f"{'Год':^5} │ {'Внесено за год':^16} │ {'Проценты/год':^16} │ {'Баланс на конец':^18}"
    print(header)
    print(divider)

    for row in schedule:
        print(
            f"{row.year:^5} │ "
            f"{row.deposited_this_year:>14,.2f} ₽ │ "
            f"{row.interest_this_year:>14,.2f} ₽ │ "
            f"{row.end_balance:>16,.2f} ₽"
        )

    print(divider)
    print(f" Всего внесено личных средств: {total_user_deposits:>16,.2f} ₽")
    print(f" Всего начислено процентов:   {total_interest:>16,.2f} ₽")
    print(f" Итоговая сумма на счету:     {final_balance:>16,.2f} ₽")
    print("═" * 68 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI калькулятор сложных процентов с поддержкой ежемесячных взносов."
    )
    parser.add_argument(
        "-p", "--principal", type=float, required=True, help="Начальная сумма (капитал)"
    )
    parser.add_argument(
        "-r", "--rate", type=float, required=True, help="Годовая процентная ставка (в %)"
    )
    parser.add_argument(
        "-y", "--years", type=int, required=True, help="Срок инвестиций в годах"
    )
    parser.add_argument(
        "-m", "--monthly", type=float, default=0.0, help="Ежемесячный взнос (по умолчанию 0)"
    )

    args = parser.parse_args()

    schedule = calculate_compound_interest(
        principal=args.principal,
        annual_rate=args.rate,
        years=args.years,
        monthly_deposit=args.monthly,
    )

    render_table(
        principal=args.principal,
        annual_rate=args.rate,
        years=args.years,
        monthly_deposit=args.monthly,
        schedule=schedule,
    )


if __name__ == "__main__":
    main()