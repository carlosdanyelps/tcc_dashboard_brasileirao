'use client';

// import { useEffect, useState } from 'react';
import './TimeList.css';
// import axios from 'axios';
import TimeCard from '../TimeCard/TimeCard';
import { useState, useEffect } from "react";
// import { Movie } from '@/app/types/movie';

interface TimeData {
  time: string;
  pontos: number;
  ano: number;
}

const TimeList = () => {

  const [dados, setDados] = useState<TimeData[]>([]); 
  const URL = "http://127.0.0.1:5000/API/campeoes_A";

  useEffect(() => {
    async function fetchData() {
      try {
        const resp = await fetch(URL);
        if (resp.ok) {
          const data = await resp.json();
          setDados(data["Campeões"]);
        }
      } catch (error) {
        console.error("Erro ao buscar API:", error);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="time-list">
    {dados.map((time, pontos, ano, index) => (
      <TimeCard key={index} dados={ano, pontos, time} />
    ))}
  </div>
  );
}

export default TimeList;