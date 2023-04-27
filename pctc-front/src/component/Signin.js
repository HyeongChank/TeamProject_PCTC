/* Level 3 */
/* Login, Join */

import './signin.css'

const Signin = () => {
  // 로그인 상태인지 아닌지에 따라 

  const popupSigninPage = (signState) => {
    switch(signState){
      case 'login': 
        window.open('./signin', 'example', 'width=800,height=600');
        break;
      case 'join':
        window.open('http://www.naver.com', 'example', 'width=800,height=600');
        break;
      default: return;
    }
  };

  return(
    <div className='signin'>
      <button className='signin-btn' onClick={() => {popupSigninPage('login')}}>Login</button>
      <button className='signin-btn' onClick={() => {popupSigninPage('join')}}>Join</button>
    </div>
  )
}

export default Signin;