/* Level 3 */
/* Congestion prediction and visualization service */
/* 혼잡도 예측 및 시각화 서비스 */
import { useEffect, useState } from 'react';
import './serviceview.css'
import Block from './component/Block';

const { kakao } = window;

const CPVS = ({ isLogin }) => {

  /**
   * Backend에서 받아야 할 혼잡도 값. 임시로 쓰는 변수.
   */
  const congestion = 0.7;
  const sizeWidth = 400;
  const sizeHeight = 70;
  const scale = 0.1;

  const [serviceViewOpacity, setServiceViewOpacity] = useState(0);

  const kakaoMap = <div id="map" style={{ width: '100%', height: '100%', opacity: serviceViewOpacity }}>
    <div id="area-1" style={{ opacity: serviceViewOpacity }} className='area-anim'></div>
    <div id="area-2" style={{ opacity: serviceViewOpacity }} className='area-anim'></div>
    <div id="area-3" style={{ opacity: serviceViewOpacity }} className='area-anim'></div>
  </div>


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
      <div id="map" style={{ width: '100%', height: '100%', opacity: serviceViewOpacity }}>
        <Block locationX='320px' locationY='410px' congestion={congestion} sizeWidth={sizeWidth} sizeHeight={sizeHeight} scale={scale} />
        <Block locationX='320px' locationY='390px' congestion={congestion} sizeWidth={sizeWidth} sizeHeight={sizeHeight} scale={scale} />
        <Block locationX='320px' locationY='360px' congestion={congestion} sizeWidth={sizeWidth} sizeHeight={sizeHeight} scale={scale} />
        <Block locationX='320px' locationY='340px' congestion={congestion} sizeWidth={sizeWidth} sizeHeight={sizeHeight} scale={scale} />
      </div>
    </div>
  )
}

export default CPVS;