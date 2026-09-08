import "./style.css";
import { useState } from "react";
import Header from "../../Components/Header/Header";

function Home() {
  const [cardAtual, setCardAtual] = useState(1);

  const cards = [
    {
      titulo: "Dados",
      texto: "Explore os dados e estatísticas disponíveis sobre os times.",
    },
    {
      titulo: "Gráficos",
      texto:
        "Visualize informações detalhadas, compare equipes e acompanhe diferentes temporadas.",
    },
    {
      titulo: "Classificação",
      texto: "Consulte classificações e dados históricos do campeonato.",
    },
    {
      titulo: "Estatísticas",
      texto: "Analise o desempenho dos clubes durante diferentes temporadas.",
    },
  ];

  const proximoCard = () => {
    setCardAtual((atual) => (atual === cards.length - 1 ? 0 : atual + 1));
  };

  const cardAnterior = () => {
    setCardAtual((atual) => (atual === 0 ? cards.length - 1 : atual - 1));
  };

  return (
    <div className="home-page">
      {/* <Header fixed={true} /> */}

      <main>
        {/* HERO */}
        <section className="hero">
          <div className="hero-overlay" />

          <div className="hero-content">
            <blockquote>
              Explore os dados, estatísticas e informações do Campeonato
              Brasileiro.
            </blockquote>

            <a href="#proposta" className="btn-primary">
              Ler mais
            </a>
          </div>
        </section>

        {/* NOSSA PROPOSTA */}
        <section className="nossa-proposta" id="proposta">
          <h2>Qual é a nossa proposta?</h2>

          <div className="proposta-grid">
            <div className="proposta-item">
              <div className="shape circle" />

              <p>
                Nosso objetivo é apresentar informações do Campeonato Brasileiro
                de uma forma visual, simples e acessível.
              </p>
            </div>

            <div className="proposta-item reverse">
              <p>
                Explore estatísticas, compare equipes e acompanhe diferentes
                temporadas através dos gráficos.
              </p>

              <div className="shape triangle" />
            </div>
          </div>
        </section>

        {/* CARDS */}
        <section className="explorar">
          <h2>Explore a plataforma</h2>

          <div className="carousel">
            <button className="arrow arrow-left" onClick={cardAnterior}>
              &#10094;
            </button>

            <div className="carousel-window">
              <div
                className="carousel-track"
                style={{
                  transform: `translateX(calc(50% - ${cardAtual * 270}px - 125px))`,
                }}
              >
                {cards.map((card, index) => (
                  <div
                    className={`card ${index === cardAtual ? "active" : ""}`}
                    key={card.titulo}
                  >
                    <h3>{card.titulo}</h3>

                    <p>{card.texto}</p>

                    {index === cardAtual && (
                      <a href="/graphics" className="btn-primary">
                        Ler mais
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <button className="arrow arrow-right" onClick={proximoCard}>
              &#10095;
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Home;
