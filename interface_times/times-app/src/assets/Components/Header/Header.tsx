// import React from 'react';
import './Header.css'

import React from 'react';
import SeletorTemp from '../Seletor/SeletorTemp';

interface TimeData {
  ano: number;
}

interface HeaderProps {
  dados: TimeData[];
  onAnoChange: (ano: number) => void;
  anoSelecionado: number;
}

const Header = ({ dados, onAnoChange, anoSelecionado }: HeaderProps) => {
  return (
    <header className='header'>
      <div className="header-logo">
        <h1>LS</h1>
      </div>
      <nav className="navbar">
        <ul>
          <li>Home</li>
          <li>Classificação</li>
          <li>Gráficos</li>       
        </ul>
      </nav>
      <SeletorTemp dados={dados} onAnoChange={onAnoChange} anoSelecionado={anoSelecionado} />
    </header>
  )
}

export default Header
