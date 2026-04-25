'use client';

import './Main.css'
import TimeList from '../TimeList/TimeList';
import ChartAPI from '../graphics/ChartAPI/ChartAPI';

interface MainProps {
  anoSelecionado: number;
}

const Main = ({ anoSelecionado }: MainProps) => {
  
    return (
      
      <div className="main">
        <div className="main-content">
          <div className='graphic-session'>
              <ChartAPI anoSelecionado={anoSelecionado} />
          </div>
          <div className='aside-content'>
              <TimeList anoSelecionado={anoSelecionado} />
          </div>
        </div>
        <div className="table">
        </div>
      </div>
    );  
}

export default Main
