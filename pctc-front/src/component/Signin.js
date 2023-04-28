/* Level 3 */
/* Login, Join */
import { useState, useEffect } from 'react'
import Modal from 'react-modal';

import './signin.css'


const Signin = ({isLogin, setIsLogin}) => {
  
  const [signinView, setSigninView] = useState();
  const [popupIsOpen, setPopupIsOpen] = useState(false);
  const [popupInfo, setPopupInfo] = useState({});

  const ModalStyle = {
    overlay: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(255,255,255,0)',
      zIndex: 10,
    },
    content: {
      backgroundColor: 'white',
      top: '200px',
      left: '675px',
      right: '675px',
      bottom: '200px',
    }
  };

  const selectFunction = (functionName) => {
    switch(functionName){
      case 'login': 
        setPopupInfo({
          'submitButtonName': "로그인",
          'content': "로그인 창",
        });
        setPopupIsOpen(true);
        break;

      case 'join': 
        setPopupInfo({
          'submitButtonName': "회원가입",
          'content': "대충 회원가입하라는 말",
        });
        setPopupIsOpen(true);
        break;

      case 'logout': 
        setIsLogin(false);
        break;

      case 'mypage':
        setPopupInfo({
          'submitButtonName': "닫기",
        });
        setPopupIsOpen(true);
        break;

      case 'close':
        switch(popupInfo.submitButtonName){
          case '로그인':
            /* 실제 로그인 로직 구현 */
            setIsLogin(true); // 임시로 만든 로그인 세션
            break;

          case '회원가입':
            /* 실제 회원가입 로직 구현 */
            break;
          
          default: break;
        }
        setPopupIsOpen(false);
        break;

      default: return;
    }
  }

  useEffect(() => {
    if(isLogin){
      setSigninView(
        <>
          <Modal style={ModalStyle} isOpen={popupIsOpen} >
            {popupInfo.content}
            <button onClick={()=> selectFunction('close')}>{popupInfo.submitButtonName}</button>
          </Modal>
          <button className='signin-btn' onClick={() => {selectFunction('mypage')}}>My Page</button>
          <button className='signin-btn' onClick={() => {selectFunction('logout')}}>Logout</button>
        </>
      )
    } else {
      setSigninView(
        <>
          <Modal style={ModalStyle} isOpen={popupIsOpen} >
            {popupInfo.content}
            <button onClick={()=> selectFunction('close')}>{popupInfo.submitButtonName}</button>
          </Modal>
          <button className='signin-btn' onClick={() => {selectFunction('login')}}>Login</button>
          <button className='signin-btn' onClick={() => {selectFunction('join')}}>Join</button>
        </>
      )
    }
  }, [isLogin, signinView, popupInfo]);

  const popupSigninPage = (signState) => {
    switch(signState){
      case 'login': 
        window.open('./login', 'example', 'width=800,height=600');
        break;
      case 'join':
        window.open('./join', 'example', 'width=800,height=600');
        break;
      default: return;
    }
  };

  return(
    <div className='signin'>
      {signinView}
    </div>
  )
}

export default Signin;