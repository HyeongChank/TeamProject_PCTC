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
      if (typeof window !== "undefined") {
        const { kakao } = window;
        const standardPoint = [35.104516, 129.095172];
        console.log("kakao >> ", kakao);
        kakao.maps.load(() => {
          const mapContainer = document.getElementById("container");
          const mapOption = {
            center: new kakao.maps.LatLng(
              standardPoint[0] + 0.0025,
              standardPoint[1]
            ),
            level: 4,
            draggable: false,
            disableDoubleClickZoom: true,
          };
          const map = new kakao.maps.Map(mapContainer, mapOption);
          map.addOverlayMapTypeId(kakao.maps.MapTypeId.TERRAIN);
        });
      }
    };

  }, [container]);

  return (
    <>

      <div id='cpvs'>
        <div id="container" ref={container} />
      </div>
      <style jsx>{`
      #cpvs {
        width: 40vw;
        height 80vh;
        display: flex;
        justify-content: center;
        margin-top: 2rem;
        margin-right: 1rem;
      }
      #container {
        width: 40vw;
        height: 80vh;
        opacity: ${serviceViewOpacity};
        border: solid 1px #282828;
        border-radius: 7px;
      }
    `}</style>
    </>
  )
}

export default CPVS;