from sqlalchemy import Column, Integer, String, Date, Time, Numeric
from .db import Base


class CampeonatoBrasileiro(Base):
    __tablename__ = "campeonato_brasileiro"

    id = Column(Integer, primary_key=True)
    rodata = Column(Numeric)
    data = Column(Date)
    hora = Column(Time)

    mandante = Column(String)
    visitante = Column(String)

    formacao_mandante = Column(String)
    formacao_visitante = Column(String)

    tecnico_mandante = Column(String)
    tecnico_visitante = Column(String)

    vencedor = Column(String)
    arena = Column(String)

    mandante_placar = Column(Integer)
    visitante_placar = Column(Integer)

    mandante_estado = Column(String)
    visitante_estado = Column(String)

    rodata_x = Column(Numeric)
    partida_id = Column(String)
    rodata_y = Column(Numeric)

    clube = Column(String)
    atleta = Column(String)
    minuto = Column(String)
    tipo_de_gol = Column(String)

    ano_civil = Column(Integer)
    temporada = Column(Integer)

    rodata_calculada = Column(Numeric)
    rodata_final = Column(Numeric)
    rodata_corrigida = Column(Numeric)
    temporada_corrigida = Column(Integer)   