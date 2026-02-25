import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import date
from app import db

class EnergyLog(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    business_name: so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False)

    log_date: so.Mapped[date] = so.mapped_column(nullable=False)
    use_for: so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False)  # e.g. freezers
    kwh: so.Mapped[float] = so.mapped_column(nullable=False)
    cost: so.Mapped[float] = so.mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<EnergyLog {self.id} {self.business_name} {self.log_date}>"
