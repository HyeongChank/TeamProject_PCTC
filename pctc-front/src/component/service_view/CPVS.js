/* Level 3 */
/* Congestion prediction and visualization service */
/* 혼잡도 예측 및 시각화 서비스 */
import { useEffect, useState } from 'react';
import BarChart from './component/BarChart';
import './serviceview.css'
import { UserData } from './component/Data';

const { kakao } = window;

const CPVS = ({ isLogin }) => {

  const [serviceViewOpacity, setServiceViewOpacity] = useState(0);

  const kakaoMap = <div id="map" style={{ width: '100%', height: '100%', opacity: serviceViewOpacity }}>
    <div id="area-1" style={{opacity: serviceViewOpacity}} className='area-anim'></div>
    <div id="area-2" style={{opacity: serviceViewOpacity}} className='area-anim'></div>
    <div id="area-3" style={{opacity: serviceViewOpacity}} className='area-anim'></div>
  </div>

  const [userData, setUserData] = useState({
    labels: UserData.map((x) => x.year),
    datasets: [{
      label: "Users Gained",
      data: UserData.map((x) => x.userGain),
    }, {
      label: "Users Gained2",
      data: UserData.map((x) => x.userLost),
    }]
  });

  useEffect(() => {
    if (isLogin) {
      setServiceViewOpacity(1)
      var container = document.getElementById('map');
      var options = {
        center: new kakao.maps.LatLng(35.106, 129.08),
        level: 4,
        draggable: false,
        disableDoubleClickZoom: true,
      };

      var map = new kakao.maps.Map(container, options);
    } else {
      setServiceViewOpacity(0)
    }
  }, [isLogin]);

  return (
    <div className='cpvs'>
      {/* <div style={{ 'fontSize': '2em', fontWeight: 'bold', textAlign: 'center' }}>CPVS Area</div> */}
      {kakaoMap}
      {/* <div style={{ width: '700px', height: '700px' }}>
        <BarChart chartData={userData} />
      </div> */}
    </div>
  )
}

export default CPVS;