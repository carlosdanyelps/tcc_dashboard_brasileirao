'use client'

// import React from 'react'
import './SeletorTemp.css'

interface TimeData {
    ano: number;
}

interface TimeSeletorProps {
    dados: TimeData[];
    onAnoChange: (ano: number) => void;
    anoSelecionado: number;
}

const SeletorTemp = ({ dados, onAnoChange, anoSelecionado }: TimeSeletorProps) => {
    return (
        <select className='selector' name="ano" id="temporada" value={anoSelecionado} onChange={(e) => onAnoChange(Number(e.target.value))}>
          <option value="" disabled>Selecione uma temporada</option>
          {dados.map((item) => (
            <option key={item.ano} value={item.ano}>
                {item.ano}
            </option>
          ))}
        </select>
    )
}

export default SeletorTemp
