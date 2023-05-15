'use client'
import Script from 'next/script';
import { useEffect, useRef, useState } from 'react';

const { kakao } = window;

const CPVS = () => {

  const [serviceViewOpacity, setServiceViewOpacity] = useState(1);
  const container = useRef(null);
  // useEffect(() => {
  //   if (isLogin) {
  //     setServiceViewOpacity(1)
  //     var container = document.getElementById('map');
  //     var options = {
  //       center: new kakao.maps.LatLng(35.106, 129.08),
  //       level: 4,
  //       draggable: false,
  //       disableDoubleClickZoom: true,
  //     };

  //     var map = new kakao.maps.Map(container, options);
  //   } else {
  //     setServiceViewOpacity(0)
  //   }
  // }, [isLogin]);

  useEffect(() => {
    const script = document.createElement('script');
    // 스크립트를 동적으로 로드하기 위해 autoload=false 파라미터 사용
    script.src = '//dapi.kakao.com/v2/maps/sdk.js?appkey=0ed00b3cb3e60ff887b0375a881a9b12&autoload=false';
    document.head.appendChild(script);

    script.onload = () => {
      kakao.maps.load(() => {
        const mapContainer = document.getElementById('container'); // 지도를 표시할 div
        const mapOption = {
          center: new kakao.maps.LatLng(37.402054, 127.108209), // 지도의 중심좌표
          level: 3 // 지도의 확대 레벨
        };

        // 지도를 표시할 div와  지도 옵션으로  지도를 생성합니다
        const map = new kakao.maps.Map(mapContainer, mapOption);
      });
    };

  }, [container]);



  return (
    <>

      <div className='cpvs'>
        {/* <div id="map" style={{ width: '100%', height: '100%', opacity: serviceViewOpacity }}></div> */}
        <div id="container" ref={container} />
      </div>

    </>
  )
}

export default CPVS;