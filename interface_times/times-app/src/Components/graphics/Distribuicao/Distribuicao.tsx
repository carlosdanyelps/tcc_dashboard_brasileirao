import { useEffect, useState } from "react";
import "./Distribuicao.css";

interface DistribuicaoProps {
  anoSelecionado: number;
}

interface DadoApi {
  time: string;
  pontos: number;
  vitorias: number;
  empates: number;
  derrotas: number;
}

const Distribuicao = ({ anoSelecionado }: DistribuicaoProps) => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const url = `http://127.0.0.1:5000/tabela?ano=${anoSelecionado}`;
        const response = await fetch(url);
        const json = await response.json();

        const dadosApi: DadoApi[] = Array.isArray(json)
          ? json
          : json["Campeoes todas temporadas"] || json["campeoes"] || [];

        if (dadosApi.length > 0) {
          const totalTimes = dadosApi.length;
          const totalPontos = dadosApi.reduce((acc, item) => acc + item.pontos, 0);
          const mediaPontos = (totalPontos / totalTimes).toFixed(1);

          const campeao = dadosApi[0];
          const rebaixado = dadosApi[dadosApi.length - 1];

          setStats({
            totalTimes,
            mediaPontos,
            pontosCampeao: campeao.pontos,
            pontosRebaixado: rebaixado.pontos,
            campeao: campeao.time,
            rebaixado: rebaixado.time,
          });
        }
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [anoSelecionado]);

  if (loading) {
    return <div className="distribuicao-loading">Carregando...</div>;
  }

  return (
    <div className="distribuicao-container">
      <div className="chart-header">
        <h2>Estatísticas Gerais</h2>
        <p>Temporada {anoSelecionado}</p>
      </div>

      {stats ? (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">🏆</div>
            <div className="stat-content">
              <h3>{stats.totalTimes}</h3>
              <p>Times na Competição</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <h3>{stats.mediaPontos}</h3>
              <p>Média de Pontos</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⭐</div>
            <div className="stat-content">
              <h3>{stats.pontosCampeao}</h3>
              <p>Pontos do Campeão</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📉</div>
            <div className="stat-content">
              <h3>{stats.pontosRebaixado}</h3>
              <p>Pontos do Último</p>
            </div>
          </div>

          <div className="stat-highlight campeao">
            <p className="stat-label">🥇 Campeão</p>
            <p className="stat-value">{stats.campeao}</p>
          </div>

          <div className="stat-highlight rebaixado">
            <p className="stat-label">📍 Última Colocação</p>
            <p className="stat-value">{stats.rebaixado}</p>
          </div>
        </div>
      ) : (
        <p>Erro ao carregar dados</p>
      )}
    </div>
  );
};

export default Distribuicao;
