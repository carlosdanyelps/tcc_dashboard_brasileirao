// import React from 'react';
import { Link } from "react-router-dom";
import "./Header.css";

interface HeaderProps {
  fixed?: boolean;
}

const Header = ({
  fixed = false,
}: HeaderProps) => {
  return (
    <header className={`header ${fixed ? "fixed" : ""}`}>
      <div className="header-logo">
        <h1>LS</h1>
      </div>
      <nav className="navbar">
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/graphics">Gráficos</Link>
          </li>
          <li>
            <Link to="/classification">Classificação</Link>
          </li>
<<<<<<< HEAD
=======
          <li>
            <Link to="/players-coaches">Jogadores e técnicos</Link>
          </li>
          <li>
            <Link to="/head-to-head">Confrontos</Link>
          </li>
<<<<<<< HEAD
>>>>>>> parent of 87020e5 (sla)
=======
>>>>>>> parent of 87020e5 (sla)
        </ul>
      </nav>
    </header>
  );
};

export default Header;
