'use client'

// import React from 'react'
import './TimeCard.css'

interface TimeData {
    time: string;
    pontos: number;
    ano: number;
}

interface TimeCardProps {
    dados: TimeData[];
}

const TimeCard = ({ dados }: TimeCardProps) => {
    return (
        <li className="time-card">
            <div className="time-icon">
                {/* Aqui você pode colocar um logo ou algo relacionado ao time */}
                <img
                    //   src={`https://image.tmdb.org/t/p/original`}
                    //   alt={item.time}
                    className="time-logo"
                />
            </div>

            <div className="time-info">
                <h3>{dados.time}</h3>
                <p>Ano: {dados.ano}</p>
                <p>Pontos: {dados.pontos}</p>
                
            </div>
        </li>
    )
}

export default TimeCard
