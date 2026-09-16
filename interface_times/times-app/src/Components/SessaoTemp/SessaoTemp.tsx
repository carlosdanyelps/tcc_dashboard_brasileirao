// import React from 'react';
import { Link } from "react-router-dom";
import "./SessaoTemp.css";

import SeletorTemp from "../Seletor/SeletorTemp";

interface TimeData {
  ano: number;
}

interface HeaderProps {
  dados: TimeData[];
  onAnoChange: (ano: number) => void;
  anoSelecionado: number;
  fixed?: boolean;
}

const SessaoTemp = ({
  dados,
  onAnoChange,
  anoSelecionado,
}: HeaderProps) => {
  return (
    <section>
      
      <SeletorTemp
        dados={dados}
        onAnoChange={onAnoChange}
        anoSelecionado={anoSelecionado}
      />
    </section>
  );
};

export default SessaoTemp;
