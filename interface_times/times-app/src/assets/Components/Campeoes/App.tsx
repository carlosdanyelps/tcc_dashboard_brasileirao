'use client';

import "../Campeoes/App.css"
import { useState, useEffect } from "react";

export default function App() {
  const [dados, setDados] = useState<any[]>([]); // estado para guardar a resposta
  const URL = "http://127.0.0.1:5000/API/campeoes_A";

  useEffect(() => {
    async function fetchData() {
      try {
        const resp = await fetch(URL);
        if (resp.ok) {
          const data = await resp.json();
          setDados(data["Campeões"]); // salva os dados no estado
        }
      } catch (error) {
        console.error("Erro ao buscar API:", error);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="content">
      <h1>Times Campeões</h1>
      <ul>
        {dados.map((item, index) => (
          <li key={index}>
            {item.ano} - {item.time} ({item.pontos} pontos)
          </li>
        ))}
      </ul>
    </div>
  );
}

