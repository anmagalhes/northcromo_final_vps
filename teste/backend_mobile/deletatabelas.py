from sqlalchemy import MetaData
from app.core.database import engine
meta = MetaData(bind=engine)
meta.reflect()
meta.drop_all()
print("Todas as tabelas foram deletadas.")
