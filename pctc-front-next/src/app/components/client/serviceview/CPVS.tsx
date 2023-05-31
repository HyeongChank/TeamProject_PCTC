'use client'

import { useEffect, useRef, useState } from 'react';
import { createBlocks } from './createBlocks';

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

            /**
             * 임의로 지정한 변수. 추후 실제 input data에 맞게 바꿔야.
             */
            let blockStatus = {
              "1A": Math.random(),
              "1B": Math.random(),
              "1C": Math.random(),
              "1D": Math.random(),
              "1E": Math.random(),
              "2A": Math.random(),
              "2B": Math.random(),
              "2C": Math.random(),
              "2D": Math.random(),
              "2E": Math.random(),
            };
            /**
             * 맵 객체를 전달하여 여러개의 블록을 그리는 함수
             */
            createBlocks(
              kakao,
              [standardPoint[0], standardPoint[1]],
              new kakao.maps.LatLng(standardPoint[0], standardPoint[1]),
              [120, 50],
              5,
              map,
              1,
              blockStatus
            );
            createBlocks(
              kakao,
              [standardPoint[0], standardPoint[1] + 0.001],
              new kakao.maps.LatLng(
                standardPoint[0] + 0.0001,
                standardPoint[1] + 0.002
              ),
              [120, 50],
              5,
              map,
              2,
              blockStatus
            );
        });
      }
    };

  }, [container, apiKey]);

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