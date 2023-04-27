/* Level 2 */

import Signin from "./Signin";
import './componentstyle.css'

const TitleView = () => {
  return(
    <div className='titleview'>
      <span className='logo'>Logo(추후IMG로 변경)</span>
      <Signin />
    </div>
  )
}

export default TitleView;