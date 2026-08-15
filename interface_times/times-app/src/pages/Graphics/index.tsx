import "./style.css";
import { useState } from "react";
import Header from "../../Components/Header/Header";
import PontosTemp from "../../Components/graphics/PontosTemp/PontosTemp.tsx";
import ComparativosTimes from "../../Components/graphics/ComparativoTimes/ComparativosTimes.tsx";

interface TimeData {
  ano: number;
}

function Graphics() {
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
      <Header
        dados={dados}
        onAnoChange={handleAnoChange}
        anoSelecionado={anoSelecionado}
      />
      <div className="main-content">
        <div className="graphic-session">
          <PontosTemp anoSelecionado={anoSelecionado} />
        </div>
        <div className="top4-session">
          <ComparativosTimes anoSelecionado={anoSelecionado} />
        </div>
      </div>
    </>
  );
}

export default Graphics;
