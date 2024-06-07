from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import Field
from workout_api.contrib.models import BaseModel
from typing import List

class AtletaModel(BaseModel):
    __tablename__ = 'atletas'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    categoria: Mapped['CategoriaModel'] = relationship(back_populates="atleta", lazy='selectin')
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.pk_id"))
    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates="atleta", lazy='selectin')
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey("centros_treinamento.pk_id"))

class AtletaCustom(BaseModel):
    id: int
    nome: str
    centro_treinamento: str = Field(..., description='Nome do centro de treinamento')
    categoria: str = Field(..., description='Nome da categoria do atleta')

@router.get(
    '/', 
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=List[AtletaCustom],
)
async def query(
    db_session: DatabaseDependency,
    nome: str = Query(None, description='Filtrar atletas por nome'),
    cpf: str = Query(None, description='Filtrar atletas por CPF'),
    limit: int = Query(10, description='Número máximo de resultados a serem retornados'),
    offset: int = Query(0, description='Número de resultados a serem ignorados no início'),
) -> List[AtletaCustom]:
    query = select(AtletaModel)
    if nome:
        query = query.filter(AtletaModel.nome.ilike(f'%{nome}%'))
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    atletas: List[AtletaModel] = (await db_session.execute(query.limit(limit).offset(offset))).scalars().all()
    
    return [{
        'id': atleta.pk_id,
        'nome': atleta.nome,
        'centro_treinamento': atleta.centro_treinamento.nome,
        'categoria': atleta.categoria.nome
    } for atleta in atletas]
