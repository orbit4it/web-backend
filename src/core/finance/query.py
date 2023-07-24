import datetime
from typing import List
from sqlalchemy import func, or_, text
from sqlalchemy.sql import extract
import strawberry
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from strawberry.types import Info

from helpers.types import Success, Error
from permissions.auth import UserAuth

from . import model, type as type


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[UserAuth], description="(Login ) list transaksi kas"
    )
    def balances(
        self,
        info: Info,
        search: str = "",
        limit: int = 20,
        page: int = 1,
        order_by: str = "date",
        sort: str = "asc",
    ) -> List[type.BalanceType]:
        db: Session = info.context["db"]

        query = (
            db.query(model.Balance).filter(or_(model.Balance.title.like(f"%{search}%")))
            if search != ""
            else db.query(model.Balance)
        )

        return (
            query.order_by(text(order_by + " " + sort))
            .offset((page - 1) * limit)
            .limit(limit)
        )

    @strawberry.field(
        permission_classes=[UserAuth],
        description="(Login) total pemasukan, pengeluaran, dan saldo",
    )
    def balance_totals(self, info: Info) -> type.BalanceTotals:
        db: Session = info.context["db"]

        total_income = (
            db.query(func.sum(model.Balance.amount).label("total"))
            .filter(model.Balance.flow == type.CashFlow.MASUK)
            .first()
        )
        total_outcome = (
            db.query(func.sum(model.Balance.amount).label("total"))
            .filter(model.Balance.flow == type.CashFlow.KELUAR)
            .first()
        )

        return type.BalanceTotals(
            total_income=total_income[0],
            total_outcome=total_outcome[0],
            total_balance=(total_income[0] - total_outcome[0]),
        )

    @strawberry.field(
        permission_classes=[UserAuth],
        description="(Login) data untuk grafik saldo keuangan",
    )
    def balance_graph(
        self, info: Info, filter_by: str = "week"
    ) -> type.BalanceGraph | Error:
        db: Session = info.context["db"]

        income = []
        outcome = []
        now = datetime.datetime.now()
        month = now.month
        year = now.year

        def extract_by(by, flow):
            return db.query(
                extract(by, model.Balance.date).label("time"),
                func.sum(model.Balance.amount).label("total"),
            ).filter(model.Balance.flow == flow)

        if filter_by == "week":

            def extract_by_week(flow):
                return (
                    extract_by("week", flow)
                    .filter(extract("month", model.Balance.date) == month)
                    .filter(extract("year", model.Balance.date) == year)
                    .group_by(extract("week", model.Balance.date))
                    .order_by(extract("week", model.Balance.date))
                    .all()
                )

            income = extract_by_week(type.CashFlow.MASUK)
            outcome = extract_by_week(type.CashFlow.KELUAR)

        elif filter_by == "month":

            def extract_by_month(flow):
                return (
                    extract_by("month", flow)
                    .filter(extract("year", model.Balance.date) == year)
                    .group_by(extract("month", model.Balance.date))
                    .all()
                )

            income = extract_by_month(type.CashFlow.MASUK)
            outcome = extract_by_month(type.CashFlow.KELUAR)

        elif filter_by == "year":

            def extract_by_year(flow):
                return (
                    extract_by("year", flow)
                    .filter(extract("year", model.Balance.date) >= (year - 5))
                    .group_by(extract("year", model.Balance.date))
                    .all()
                )

            income = extract_by_year(type.CashFlow.MASUK)
            outcome = extract_by_year(type.CashFlow.KELUAR)

        else:
            return Error("Pilihan filter waktu tidak valid")

        return type.BalanceGraph(income=income, outcome=outcome)
