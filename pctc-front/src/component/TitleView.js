/* Level 2 */

import Signin from "./signin/Signin";
import './componentstyle.css'
import logo from '../assets/logo.png'
import { Link } from "react-router-dom";

const TitleView = (props) => {
  return(
    <div className='titleview'>
      <Link to='/'><img className="titleview-logo" src={logo} alt="logo" /></Link>
      <div style={{'fontSize': '2em', fontWeight:'bold', textAlign: 'center'}}>TitleView Area</div>
      <Signin isLogin={props.isLogin} setIsLogin={props.setIsLogin} />
    </div>
  )
}

export default TitleView;