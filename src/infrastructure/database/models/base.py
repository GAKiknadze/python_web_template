from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')


__all__ = ["Base"]
