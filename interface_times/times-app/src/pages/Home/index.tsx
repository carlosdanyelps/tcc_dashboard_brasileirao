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
    <>
      <div className="home-page">
        <Header
          dados={dados}
          onAnoChange={handleAnoChange}
          anoSelecionado={anoSelecionado}
          fixed={true}
        />

        <main>
          <section className="hero">
            <div className="hero-overlay"></div>

            <div className="container hero-content">
              <blockquote>
                Lorem ipsum dolor sit amet consectetur adipisicing elit.
                Explicabo, voluptatum!
              </blockquote>

              <a href="#" className="btn-primary">
                Ver gráficos
              </a>
            </div>
          </section>
          <section className="nossa-proposta">
            <h1>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. At
              inventore minus expedita nisi iusto quos id recusandae corporis
              natus? Debitis facere provident ad illo quidem, asperiores maiores
              corporis excepturi ipsa sit, fuga rerum dolor. Explicabo eligendi
              sed, eius nesciunt sequi ex, consequuntur deserunt necessitatibus
              tempora ipsam, quia quos provident eveniet neque cum eos quidem
              numquam inventore in similique? Rerum, alias architecto? Tenetur
              aliquam deleniti facilis ut sequi hic. Tempora ea consequatur
              repellendus praesentium soluta itaque sapiente quae, sint quos
              ratione aliquid in eligendi! Assumenda ducimus maxime, eius
              consectetur asperiores voluptatum neque molestiae autem, dicta est
              similique deleniti perferendis, fugiat nostrum praesentium hic
              odit sit soluta ullam amet. Doloribus magni hic delectus esse
              corrupti error eius quae tempore eos, minima omnis aspernatur
              illum sint aliquid eum quis tenetur molestiae repellat suscipit
              laudantium voluptates rem odit dolores commodi! Quae quam rerum
              qui aut quaerat, laborum eaque ex ipsam exercitationem dolor quasi
              temporibus explicabo laboriosam sed mollitia rem culpa
              perferendis? Placeat laudantium praesentium ipsa libero eligendi
              veritatis veniam quam quaerat repellat cum, sunt enim illum! Quae
              quibusdam necessitatibus dolor in saepe blanditiis facere officia
              ut quaerat sint tempore provident voluptates ipsam at optio
              laudantium praesentium maiores quam alias omnis, sunt assumenda
              itaque asperiores. Minus inventore labore nihil blanditiis aperiam
              ipsam, sint asperiores, nam nulla, quia quos corporis temporibus
              pariatur sit praesentium similique repellendus. Fugiat praesentium
              corporis doloremque aperiam, ex repellendus nihil eaque, nostrum
              dolore itaque hic omnis est similique cumque ducimus magnam.
              Voluptates labore sapiente omnis asperiores quas eligendi,
              incidunt distinctio explicabo nulla perspiciatis eveniet vitae
              voluptatem? Officiis voluptate necessitatibus consequuntur commodi
              enim magni autem odio quos vero placeat, fugit culpa eveniet
              voluptatibus minima dolor? Aspernatur ducimus natus magnam
              sapiente illum qui optio deserunt! Voluptas voluptate distinctio
              pariatur, quae, iusto explicabo numquam dicta similique, quasi
              perferendis qui quod? Laudantium quae, quasi sapiente sint quam
              debitis hic, excepturi natus voluptas fugiat vitae labore quisquam
              dolores dicta possimus? Nam eius repellat voluptatibus repudiandae
              facilis nemo nihil. Quas architecto ab repudiandae. Facilis
              numquam soluta quae quasi, quod laboriosam sit non, doloribus odio
              excepturi veritatis explicabo nihil. Vel id nisi eos repellat sint
              facilis dignissimos cupiditate enim laboriosam nulla mollitia
              sequi ducimus totam vitae quam itaque officiis, soluta distinctio
              corporis impedit nihil! Nemo ipsa dolore est ratione odit saepe
              quidem voluptatem! Minus, provident, saepe at, velit voluptatum
              aliquid ipsam eveniet accusantium veritatis omnis nam quos. Culpa
              tempore, quam exercitationem placeat atque fuga unde sequi
              asperiores laboriosam consequuntur, aliquid est iure, voluptatibus
              voluptate quos ut neque? Sequi quidem aliquid assumenda vel fuga
              sit temporibus quasi animi excepturi iure cupiditate enim culpa
              molestiae accusamus nesciunt repellat quis laudantium voluptate
              ipsum architecto, labore quisquam doloribus harum. Exercitationem
              molestiae quibusdam eius! Debitis labore nemo libero ipsam
              repellendus voluptate est iste obcaecati aut fuga, quisquam
              placeat nisi nihil facilis temporibus consequuntur doloremque
              aspernatur inventore praesentium voluptates! Ipsa non est aliquam
              repellat magnam saepe, quod, necessitatibus autem modi ullam illum
              doloremque, perspiciatis nisi quae quis. Commodi sequi quisquam
              laborum accusamus recusandae pariatur distinctio maxime dolor.
              Ipsum atque vel fuga beatae neque reiciendis nihil.
            </h1>
          </section>
        </main>
      </div>
    </>
  );
}

export default Home;
