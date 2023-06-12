"use client";

import { useEffect, useRef, useState } from "react";
import { createBlocksYardStatus } from "./createBlocksYardStatus";

declare global {
  interface Window {
    kakao: any;
  }
}

const YardStatus = ({ apiKey }: any) => {
  const [serviceViewOpacity, setServiceViewOpacity] = useState(1);
  const [blockStatus, setBlockStatus] = useState({});
  const container = useRef(null);

  useEffect(() => {
    (async function () {
      const res = await fetch("http://10.125.121.222:8080/yard");
      const result = await res.json();
      setBlockStatus(result);
    })();
  }, []);

  useEffect(() => {
    const script = document.createElement("script");
    script.src =
      "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + apiKey + "&autoload=false";
    document.head.appendChild(script);

    script.onload = () => {
      if (typeof window !== "undefined") {
        const { kakao } = window;
        const standardPoint = [35.104516, 129.095172];
        kakao.maps.load(() => {
          const mapContainer = document.getElementById("container");
          const mapOption = {
            center: new kakao.maps.LatLng( // 지도의 기준점
              standardPoint[0] + 0.0025,
              standardPoint[1]
            ),
            level: 4,
            draggable: false,
            disableDoubleClickZoom: true,
          };
          const map = new kakao.maps.Map(mapContainer, mapOption);
          map.addOverlayMapTypeId(kakao.maps.MapTypeId.TERRAIN);
          map.addOverlayMapTypeId(kakao.maps.MapTypeId.TRAFFIC);

          /**
           * 맵 객체를 전달하여 여러개의 블록을 그리는 함수
           */
          createBlocksYardStatus(
            kakao,
            new kakao.maps.LatLng(
              standardPoint[0] + 0.0045,
              standardPoint[1] - 0.0005
            ),
            [75, 25],
            9,
            map,
            1,
            blockStatus
          );
          createBlocksYardStatus(
            kakao,
            new kakao.maps.LatLng(
              standardPoint[0] + 0.004,
              standardPoint[1] - 0.00045
            ),
            [75, 25],
            9,
            map,
            2,
            blockStatus
          );
          createBlocksYardStatus(
            kakao,
            new kakao.maps.LatLng(
              standardPoint[0] + 0.0035,
              standardPoint[1] - 0.0004
            ),
            [75, 25],
            11,
            map,
            3,
            blockStatus
          );
          createBlocksYardStatus(
            kakao,
            new kakao.maps.LatLng(
              standardPoint[0] + 0.003,
              standardPoint[1] - 0.00035
            ),
            [75, 25],
            9,
            map,
            4,
            blockStatus
          );
          createBlocksYardStatus(
            kakao,
            new kakao.maps.LatLng(
              standardPoint[0] + 0.0025,
              standardPoint[1] - 0.0003
            ),
            [75, 25],
            8,
            map,
            5,
            blockStatus
          );
          createBlocksYardStatus(
            kakao,
            new kakao.maps.LatLng(
              standardPoint[0] + 0.002,
              standardPoint[1] - 0.00025
            ),
            [75, 25],
            6,
            map,
            6,
            blockStatus
          );
          createBlocksYardStatus(
            kakao,
            new kakao.maps.LatLng(
              standardPoint[0] + 0.0015,
              standardPoint[1] - 0.0002
            ),
            [75, 25],
            7,
            map,
            7,
            blockStatus
          );
          createBlocksYardStatus(
            kakao,
            new kakao.maps.LatLng(
              standardPoint[0] + 0.001,
              standardPoint[1] - 0.00015
            ),
            [75, 25],
            7,
            map,
            8,
            blockStatus
          );
          createBlocksYardStatus(
            kakao,
            new kakao.maps.LatLng(
              standardPoint[0] + 0.0005,
              standardPoint[1] - 0.0001
            ),
            [75, 25],
            7,
            map,
            9,
            blockStatus
          );
        });
      }
    };
  }, [container, apiKey, blockStatus]);

  return (
    <>
      <div id="yard-status">
        <div id="container" ref={container} />
      </div>
      <style jsx>{`
      #yard-status {
        width: 80vw;
        height 80vh;
        display: flex;
        justify-content: center;
      }
      #container {
        width: 80vw;
        height: 80vh;
        opacity: ${serviceViewOpacity};
        border: solid 1px #282828;
        border-radius: 7px;
      }
    `}</style>
    </>
  );
};

export default YardStatus;
