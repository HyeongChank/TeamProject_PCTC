/* Level 2 */

import Signin from "./signin/Signin";
import './componentstyle.css'
import logo from '../assets/logo.png'
import { Link } from "react-router-dom";
import TitleMenu from "./TitleMenu";

const TitleView = (props) => {
  return (
    <div className='titleview'>
      <div className="titleview-logo-area">
        <Link to='/'><img className="titleview-logo" src={logo} alt="logo" /></Link>
      </div>
      <div className="titleMenus">
        <Link to='/bas'><TitleMenu name="선석배정현황" /></Link>
        <Link to='/sws'><TitleMenu name="본선작업현황" /></Link>
        <Link to='/cts'><TitleMenu name="컨테이너 반출입현황" /></Link>
        <Link to='/ctas'><TitleMenu name="컨테이너터미널 재박현황" /></Link>
        <Link to='/ctads'><TitleMenu name="컨테이너터미널 입출항현황" /></Link>
      </div>
      <Signin isLogin={props.isLogin} setIsLogin={props.setIsLogin} />
    </div>
  )
}

export default TitleView;