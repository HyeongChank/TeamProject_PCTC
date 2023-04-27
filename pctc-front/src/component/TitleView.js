/* Level 2 */

import Signin from "./Signin";
import './componentstyle.css'
import logo from '../assets/logo.png'
import { Link } from "react-router-dom";

const TitleView = () => {
  return(
    <div className='titleview'>
      <Link to='/'><img className="titleview-logo" src={logo} alt="logo" /></Link>
      <Signin />
    </div>
  )
}

export default TitleView;