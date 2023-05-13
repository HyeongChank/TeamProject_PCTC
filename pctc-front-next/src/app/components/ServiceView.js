/* Level 2 */
/* CPVS, CDDRS, SADRS를 표시하는 컴포넌트 */

import CPVS from "./service_view/CPVS";
import SADRS from "./service_view/SADRS";
import CDDRS from "./service_view/CDDRS";
import './service_view/serviceview.css'

const ServiceView = ({ isLogin }) => {
  return (
    <div className='serviceview'>
      <CPVS isLogin={isLogin} />
      <div className='serviceview-right'>
        <SADRS isLogin={isLogin} />
        <CDDRS isLogin={isLogin} />
      </div>
    </div>
  )
}

export default ServiceView;