'use client';

import './Main.css'
import ComparativosTimes from '../graphics/ComparativoTimes/ComparativosTimes.tsx';
import PontosTemp from '../graphics/PontosTemp/PontosTemp';
import Classificacao from '../Classificacao/Classificacao';

interface MainProps {
  anoSelecionado: number;
}

const Main = ({ anoSelecionado }: MainProps) => {
  
    return (
      
      <div className="main">
        <div className="main-content">
          <div className='graphic-session'>
              <PontosTemp anoSelecionado={anoSelecionado} />
          </div>
          <div className='timelist'>
              <ComparativosTimes anoSelecionado={anoSelecionado} />
          </div>
        </div>
        <div className="table">
          <Classificacao anoSelecionado={anoSelecionado} />
        </div>
      </div>
    );  
}

export default Main
