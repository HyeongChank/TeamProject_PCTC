/* Level 0 */
import React from 'react';
import { BrowserRouter as Router, Route, Link, BrowserRouter, Routes } from 'react-router-dom';

import './App.css';

import Apps from './Apps';
import Login from './component/Login';
import Home from './component/Home';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path='/' Component={Home} />
          <Route path='/signin' Component={Login} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
