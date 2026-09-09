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
        </ul>
      </nav>
    </header>
  );
};

export default Header;
