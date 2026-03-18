import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Header from './assets/Components/Header/Header.tsx'
import Main from './assets/Components/Main/Main.tsx'


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Header />
    <Main />
  </StrictMode>,
)
