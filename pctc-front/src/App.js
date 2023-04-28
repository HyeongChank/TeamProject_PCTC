/* Level 0 */
import React from 'react';
import { BrowserRouter as Router, Route, Link, BrowserRouter, Routes } from 'react-router-dom';
import { useState } from 'react'

import './App.css';

import Apps from './Apps';
import Home from './component/Home';

function App() {
  /* 로그인 상태에 따른 페이지 개발을 위해 임시로 설정한 변수입니다. */
  const [isLogin, setIsLogin] = useState(false);
  /* 로그인 상태에 따른 페이지 개발을 위해 임시로 설정한 변수입니다. */

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Home isLogin={isLogin} setIsLogin={setIsLogin} />} />
          {/* <Route path='/login' Component={Login} />
          <Route path='/join' Component={Join} /> */}
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
