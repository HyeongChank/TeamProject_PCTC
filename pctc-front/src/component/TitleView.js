/* Level 2 */

import Signin from "./Signin";
import './componentstyle.css'
import logo from '../assets/logo.png'

const TitleView = () => {
  return(
    <div className='titleview'>
      <img className="titleview-logo" src={logo} alt="logo" />
      <Signin />
    </div>
  )
}

export default TitleView;