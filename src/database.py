import logging
from datetime import datetime
from types import TracebackType
from typing import cast, override

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class Measurement(Base):
    """SQLAlchemy model for sensor measurements."""

    __tablename__: str = "measurement"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    temperature: Mapped[float]  # pyright: ignore[reportUninitializedInstanceVariable]
    humidity: Mapped[float]  # pyright: ignore[reportUninitializedInstanceVariable]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)

    @override
    def __repr__(self):
        return (
            f"<Measurement(id={self.id}, temp={self.temperature:.2f}, "
            f"humidity={self.humidity}%, timestamp={self.timestamp})>"
        )


class DatabaseManager:
    """Manages database operations for sensor measurements."""

    _db_path: str
    _engine: Engine
    _session: Session  # pyright: ignore[reportUninitializedInstanceVariable]

    def __init__(self, db_path: str = "measurements.db"):
        """
        Initialize the database manager.

        Args:
            db_path: Path to the SQLite database file
        """
        self._db_path = db_path
        self._engine = create_engine(f"sqlite:///{db_path}", echo=False)

        # Create tables
        Base.metadata.create_all(bind=self._engine)

    def __enter__(self):
        self._session = Session(self._engine)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        self._session.close()

    def insert_measurement(
        self, temperature: float, humidity: float, timestamp: datetime | None = None
    ):
        """
        Insert a new measurement into the database.

        Args:
            temperature: Temperature in Celsius
            humidity: Relative humidity percentage
            timestamp: Measurement timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now()

        measurement = Measurement(
            temperature=temperature, humidity=humidity, timestamp=timestamp
        )
        self._session.add(measurement)
        self._session.commit()
        self._session.refresh(measurement)
        logging.info(f"💾 Inserted measurement: {measurement}")

    def get_all_measurements(self) -> list[Measurement]:
        """
        Retrieve all measurements from the database.
        """
        statement = select(Measurement).order_by(Measurement.timestamp)
        all_measurements = self._session.scalars(statement).all()

        return cast(list[Measurement], all_measurements)
