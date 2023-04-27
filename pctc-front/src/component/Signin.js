/* Level 3 */
/* Login, Join */

import './signin.css'

const Signin = () => {
  // 로그인 상태인지 아닌지에 따라 

  return(
    <div className='signin'>
      <button className='signin-btn'>Login</button>
      <button className='signin-btn'>Join</button>
    </div>
  )
}

export default Signin;