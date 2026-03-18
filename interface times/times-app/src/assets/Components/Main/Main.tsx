'use client';

import './Main.css'
import TimeList from '../TimeList/TimeList';

const Main = () => {
  
    return (
      <div className="main">
        <div className='graphic-session'>
            <p>Hello</p>
        </div>
        <div className='aside-content'>
            <TimeList />
        </div>

        <div className="main-content">
        </div>
      </div>
    );
}

export default Main
