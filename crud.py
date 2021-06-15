from sqlalchemy.orm import Session

import models


def get_tax(db: Session, salary: int, detailed: bool):
    query = (
        db.query(models.Tax)
        .filter(models.Tax.amount <= salary)
        .order_by(models.Tax.amount.desc())
    )
    tax = {}
    for q in query:
        tax[f"{q.rate}% on {salary-q.amount} ({q.amount} - {salary})"] = int(
            ((salary - q.amount) * q.rate / 100)
        )
        salary = q.amount

    tax["Total"] = sum(tax.values())
    if detailed:
        return tax

    return tax["Total"]
