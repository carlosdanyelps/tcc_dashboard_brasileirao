'use client';

// import { useEffect, useState } from 'react';
import './TimeList.css';
// import axios from 'axios';
import TimeCard from '../TimeCard/TimeCard';
import { useState, useEffect } from "react";

interface TimeData {
  time: string;
  pontos: number;
  ano: number;
}

interface TimeListProps {
  anoSelecionado: number;
}

const TimeList = ({ anoSelecionado }: TimeListProps) => {

  const [dados, setDados] = useState<TimeData[]>([]); 
  const URL = `http://127.0.0.1:5000/tabela?ano=${anoSelecionado}`;

  useEffect(() => {
    async function fetchData() {
      try {
        const resp = await fetch(URL);
        if (resp.ok) {
          const data = await resp.json();
          setDados(data);
        }
      } catch (error) {
        console.error("Erro ao buscar API:", error);
      }
    }
    fetchData();
  }, [anoSelecionado]);

  return (
    <div className="time-list">
    {dados.map((time, index) => (
      <TimeCard key={index} dados={time} />
    ))}
  </div>
  );
}

export default TimeList;