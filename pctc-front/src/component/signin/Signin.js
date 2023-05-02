/* Level 3 */
/* Login, Join */
import { useState, useEffect } from 'react'
import Popup from './component/Popup';

import './signin.css'


const Signin = ({ isLogin, setIsLogin }) => {
  // isLogin : 로그인 여부
  // setIsLogin : 로그인/로그아웃

  const [signinView, setSigninView] = useState(); // 실제 Signin 컴포넌트 렌더링할 내용
  const [popupIsOpen, setPopupIsOpen] = useState(false); // 팝업창 on/off 여부
  const [popupInfo, setPopupInfo] = useState({}); // 팝업창 내용

  const translater = { // 번역기
    "kakao": "카카오",
    "naver": "네이버",
    "google": "구글",
    "카카오": "kakao",
    "네이버": "naver",
    "구글": "google",
    "로그인": "login",
    "login": "로그인",
    "회원가입": "join",
    "join": "회원가입",
  };

  const buttonFunction = (functionName, loginType) => {
    /** 실제 로그인이나 회원가입 버튼을 눌렀을 때 */
    /**  */
    selectFunction(functionName);
    setPopupIsOpen(false);

    if(functionName === 'login')
      setIsLogin(true)
  }

  const selectFunction = (functionName) => {

    switch (functionName) {
      case 'login':
        setPopupIsOpen(true);
        setPopupInfo({
          'action': " 계정으로 로그인하기",
          'content': "로그인",
        });
        break;

      case 'join':
        setPopupIsOpen(true);
        setPopupInfo({
          'action': " 계정으로 회원가입",
          'content': "회원가입",
        });
        break;

      case 'logout':
        setPopupInfo({
          'action': " 계정으로 회원가입",
          'content': "회원가입",
        });
        setIsLogin(false);
        break;

      default:
        break;
    }

  }

  useEffect(() => {
    if (isLogin) {
      setSigninView(// 로그인 상태의 Signin 컴포넌트
        <>
          <button className='signin-btn' onClick={() => selectFunction('mypage')}>My Page</button>
          <button className='signin-btn' onClick={() => selectFunction('logout')}>Logout</button>
        </>
      )
    } else {
      setSigninView(// 로그아웃 상태의 Signin 컴포넌트
        <>
          <Popup popupIsOpen={popupIsOpen} popupInfo={popupInfo} translater={translater} buttonFunction={buttonFunction} />
          <button className='signin-btn' onClick={() => selectFunction('login')}>Login</button>
          <button className='signin-btn' onClick={() => selectFunction('join')}>Join</button>
        </>
      )
    }
  }, [isLogin, signinView, popupInfo]);

  const popupSigninPage = (signState) => {
    switch (signState) {
      case 'login':
        window.open('./login', 'example', 'width=800,height=600');
        break;
      case 'join':
        window.open('./join', 'example', 'width=800,height=600');
        break;
      default: return;
    }
  };

  return (
    <div className='signin'>
      {signinView}
    </div>
  )
}

export default Signin;