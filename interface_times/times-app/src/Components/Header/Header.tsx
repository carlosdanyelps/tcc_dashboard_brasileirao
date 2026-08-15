// import React from 'react';
import { Link } from "react-router-dom"
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
          <li><Link to="/" >Home</Link></li>
          <li><Link to="/graphics" >Gráficos</Link></li>
          <li><Link to="/classification" >Classificação</Link></li>      
        </ul>
      </nav>
      <SeletorTemp dados={dados} onAnoChange={onAnoChange} anoSelecionado={anoSelecionado} />
    </header>
  )
}

export default Header
