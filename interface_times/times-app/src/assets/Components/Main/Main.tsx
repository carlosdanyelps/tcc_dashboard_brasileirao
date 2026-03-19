'use client';

import './Main.css'
import TimeList from '../TimeList/TimeList';

const Main = () => {
  
    return (
      <div className="main">
        <div className="main-content">
          <div className='graphic-session'>
              <p>Hello</p>
          </div>
          <div className='aside-content'>
              <TimeList />
          </div>
        </div>
        <div className="table">
        </div>
      </div>
    );
}

export default Main
