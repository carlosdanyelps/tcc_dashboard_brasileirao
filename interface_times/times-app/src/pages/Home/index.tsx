import "./style.css";
import { useState } from "react";
import Header from "../../Components/Header/Header";

interface TimeData {
  ano: number;
}

function Home() {
  const [anoSelecionado, setAnoSelecionado] = useState<number>(2025);

  const dados: TimeData[] = [
    { ano: 2003 },
    { ano: 2004 },
    { ano: 2005 },
    { ano: 2006 },
    { ano: 2007 },
    { ano: 2008 },
    { ano: 2009 },
    { ano: 2010 },
    { ano: 2011 },
    { ano: 2012 },
    { ano: 2013 },
    { ano: 2014 },
    { ano: 2015 },
    { ano: 2016 },
    { ano: 2017 },
    { ano: 2018 },
    { ano: 2019 },
    { ano: 2020 },
    { ano: 2021 },
    { ano: 2022 },
    { ano: 2023 },
    { ano: 2024 },
    { ano: 2025 },
  ];

  const handleAnoChange = (ano: number) => {
    setAnoSelecionado(ano);
  };

  return (
    <div className="home-page">

      <Header
        dados={dados}
        onAnoChange={handleAnoChange}
        anoSelecionado={anoSelecionado}
        fixed={true}
      />

      <main>

        {/* HERO */}
        <section className="hero">
          <div className="hero-overlay" />

          <div className="hero-content">
            <blockquote>
              Explore os dados, estatísticas e informações
              do Campeonato Brasileiro.
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
                Nosso objetivo é apresentar informações
                do Campeonato Brasileiro de uma forma
                visual, simples e acessível.
              </p>
            </div>


            <div className="proposta-item reverse">
              <p>
                Explore estatísticas, compare equipes
                e acompanhe diferentes temporadas
                através dos gráficos.
              </p>

              <div className="shape triangle" />
            </div>

          </div>

        </section>


        {/* CARDS */}
        <section className="explorar">

          <h2>Qual é a nossa proposta?</h2>

          <div className="cards-container">

            <button className="arrow">
              &#10094;
            </button>

            <div className="card">
              <p>
                Explore os dados e estatísticas
                disponíveis sobre os times.
              </p>
            </div>


            <div className="card active">
              <p>
                Visualize informações detalhadas,
                compare equipes e acompanhe
                diferentes temporadas.
              </p>

              <a href="/graficos" className="btn-primary">
                Ler mais
              </a>
            </div>


            <div className="card">
              <p>
                Consulte classificações e dados
                históricos do campeonato.
              </p>
            </div>

            <button className="arrow">
              &#10095;
            </button>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Home;