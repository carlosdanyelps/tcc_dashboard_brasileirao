// import React from 'react';
import './Header.css'

import React, { useState } from 'react';
import SeletorTemp from '../Seletor/SeletorTemp';

interface TimeData {
  ano: number;
}
const Header = () => {
  const [anoSelecionado, setAnoSelecionado] = useState<number>(2024);

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
  ];

  const handleAnoChange = (ano: number) => {
    setAnoSelecionado(ano);
  }


  return (
    <header className='header'>
      <div className="header-logo">
        <h1>LS</h1>
      </div>
      <SeletorTemp dados={dados} onAnoChange={handleAnoChange} anoSelecionado={anoSelecionado} />
    </header>
  )
}

export default Header
