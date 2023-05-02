/* Level 0 */
import React from 'react';
import { BrowserRouter as Router, Route, Link, BrowserRouter, Routes } from 'react-router-dom';
import { useState } from 'react'

import './App.css';

import Home from './component/Home';
import TitleView from './component/TitleView';
import Middle from './component/Middle';
import BAS from './component/title_menu/BAS';
import CTADS from './component/title_menu/CTADS';
import CTAS from './component/title_menu/CTAS';
import CTS from './component/title_menu/CTS';
import SWS from './component/title_menu/SWS';

function App() {
  /* 로그인 상태에 따른 페이지 개발을 위해 임시로 설정한 변수입니다. */
  const [isLogin, setIsLogin] = useState(false);
  /* 로그인 상태에 따른 페이지 개발을 위해 임시로 설정한 변수입니다. */

  return (
    <div className='rootApp'>
      <BrowserRouter>
        <TitleView isLogin={isLogin} setIsLogin={setIsLogin}/>
        <Middle />
        <Routes>
          <Route path='/' element={<Home isLogin={isLogin} setIsLogin={setIsLogin} />} />
          <Route path='/bas' element={<BAS />} />
          <Route path='/ctads' element={<CTADS />} />
          <Route path='/ctas' element={<CTAS />} />
          <Route path='/cts' element={<CTS />} />
          <Route path='/sws' element={<SWS />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
