'use client'

import { useEffect, useRef, useState } from 'react';

declare global {
  interface Window {
    kakao: any;
  }
}


const CPVS = ({apiKey}: any) => {

  const [serviceViewOpacity, setServiceViewOpacity] = useState(1);
  const container = useRef(null);

  useEffect(() => {
    const script = document.createElement('script');
    script.src = '//dapi.kakao.com/v2/maps/sdk.js?appkey=' + apiKey + '&autoload=false';
    document.head.appendChild(script);

    script.onload = () => {
      if (typeof window !== 'undefined') {
        const { kakao } = window;
        kakao.maps.load(() => {
          const mapContainer = document.getElementById('container');
          const mapOption = {
            center: new kakao.maps.LatLng(35.106, 129.08),
            level: 4,
            draggable: false,
            disableDoubleClickZoom: true,
          };
          const map = new kakao.maps.Map(mapContainer, mapOption);
        });
      }
    };

  }, [container]);

  return (
    <>

      <div id='cpvs' className='w-full h-full flex justify-center mt-10'>
        <div id="container" ref={container} />
      </div>
      <style jsx>{`
      #container {
        width: 70vw;
        height: 70vh;
        opacity: ${serviceViewOpacity};
        border: solid 1px #282828;
        border-radius: 10px;
      }
    `}</style>
    </>
  )
}

export default CPVS;