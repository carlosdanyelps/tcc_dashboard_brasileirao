import { useState, useEffect } from 'react';
import './Classificacao.css';

interface TimeClassificacao {
  posicao: number;
  time: string;
  id: number;
  vitorias: number;
  empates: number;
  derrotas: number;
  temporada: number;
  pontos: number;
  gols_pro: number;
  gols_tomados: number;
  saldo: number;
  rodada: number;
  escudo: string;
  cor: string;
  bordaCor: string;
}

interface ClassificacaoProps {
  anoSelecionado: number;
}

export default function Classificacao({ anoSelecionado }: ClassificacaoProps) {
  const [classificacao, setClassificacao] = useState<TimeClassificacao[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [erro, setErro] = useState<string | null>(null);

  // Buscar dados de classificação
  useEffect(() => {
    const fetchClassificacao = async () => {
      try {
        setLoading(true);
        setErro(null);
        const response = await fetch(`http://localhost:5000/tabela?ano=${anoSelecionado}`);
        
        if (!response.ok) {
          throw new Error(`Erro na API: ${response.status}`);
        }
        
        const data = await response.json();
        setClassificacao(data);
      } catch (error) {
        setErro(error instanceof Error ? error.message : 'Erro ao carregar classificação');
        console.error('Erro:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchClassificacao();
  }, [anoSelecionado]);

  if (loading) {
    return <div className="classificacao-container loading">Carregando classificação...</div>;
  }

  if (erro) {
    return <div className="classificacao-container erro">Erro: {erro}</div>;
  }

  return (
    <div className="classificacao-container">
      {/* <h1 className="classificacao-titulo">Classificação Série A</h1> */}
      
      <div className="tabela-wrapper">
        <table className="classificacao-tabela">
          <thead>
            <tr>
              <th className="col-posicao">Pos</th>
              <th className="col-time">Time</th>
              <th className="col-pontos">Pts</th>
              <th className="col-numero">J</th>
              <th className="col-numero">V</th>
              <th className="col-numero">E</th>
              <th className="col-numero">D</th>
              <th className="col-numero">GF</th>
              <th className="col-numero">GC</th>
              <th className="col-numero">SG</th>
            </tr>
          </thead>
          <tbody>
            {classificacao.length > 0 ? (
              classificacao.map((time, index) => {
                // Calcular jogos, vitórias, empates, derrotas
                // Por enquanto, você pode usar a rodada como aproximação de jogos
                const jogos = Math.round(time.rodada);
                

                const isTopTres = index < 4;
                const isRebaixamento = index >= 16;

                return (
                  <tr
                    key={`${time.time}-${time.temporada}`}
                    className={`
                      ${isTopTres ? 'top-tres' : ''}
                      ${isRebaixamento ? 'rebaixamento' : ''}
                    `}
                  >
                    <td className="col-posicao">
                      <span className="numero-posicao">{time.posicao}</span>
                    </td>
                    
                    <td className="col-time">
                      <div className="time-info">
                        <img
                          src={time.escudo}
                          alt={time.time}
                          className="escudo"
                          onError={(e) => {
                            const target = e.target as HTMLImageElement;
                            target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="32" height="32"%3E%3Crect fill="%23ccc" width="32" height="32"/%3E%3C/svg%3E';
                          }}
                        />
                        <span className="nome-time">{time.time}</span>
                      </div>
                    </td>
                    
                    <td className="col-pontos"><strong>{time.pontos}</strong></td>
                    <td className="col-numero">{time.rodada}</td>
                    <td className="col-numero vitoria">{time.vitorias}</td>
                    <td className="col-numero empate">{time.empates}</td>
                    <td className="col-numero derrota">{time.derrotas}</td>
                    <td className="col-numero">{time.gols_pro}</td>
                    <td className="col-numero">{time.gols_tomados}</td>
                    <td className="col-numero saldo">
                      <span className={time.saldo > 0 ? 'positivo' : time.saldo < 0 ? 'negativo' : ''}>
                        {time.saldo > 0 ? '+' : ''}{time.saldo}
                      </span>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={10} className="sem-dados">
                  Nenhum dado disponível para esta temporada
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="classificacao-legenda">
        <div className="legenda-item top-tres"><aside className="libertadores"></aside> Libertadores</div>
        <div className="legenda-item rebaixamento"><aside className="rebaixado"></aside> Rebaixamento</div>
      </div>
    </div>
  );
}
