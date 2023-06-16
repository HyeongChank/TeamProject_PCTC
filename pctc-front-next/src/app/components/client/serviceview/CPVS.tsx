"use client";

import { useEffect, useRef, useState } from "react";
import { createBlocks } from "./createBlocks";

declare global {
  interface Window {
    kakao: any;
  }
}

const CPVS = ({ apiKey }: any) => {
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
           * 임의로 지정한 변수. 추후 실제 input data에 맞게 바꿔야.
           */
          // let blockStatus = {
          //   "1A": Math.random(),
          //   "1B": Math.random(),
          //   "1C": Math.random(),
          //   "1D": Math.random(),
          //   "1E": Math.random(),
          //   "1F": Math.random(),
          //   "1G": Math.random(),
          //   "1H": Math.random(),
          //   "1I": Math.random(),
          //   "2A": Math.random(),
          //   "2B": Math.random(),
          //   "2C": Math.random(),
          //   "2D": Math.random(),
          //   "2E": Math.random(),
          //   "2F": Math.random(),
          //   "2G": Math.random(),
          //   "2H": Math.random(),
          //   "2I": Math.random(),
          //   "3A": Math.random(),
          //   "3B": Math.random(),
          //   "3C": Math.random(),
          //   "3D": Math.random(),
          //   "3E": Math.random(),
          //   "3F": Math.random(),
          //   "3G": Math.random(),
          //   "3H": Math.random(),
          //   "3I": Math.random(),
          //   "3J": Math.random(),
          //   "3K": Math.random(),
          //   "4A": Math.random(),
          //   "4B": Math.random(),
          //   "4C": Math.random(),
          //   "4D": Math.random(),
          //   "4E": Math.random(),
          //   "4F": Math.random(),
          //   "4G": Math.random(),
          //   "4H": Math.random(),
          //   "4I": Math.random(),
          //   "5A": Math.random(),
          //   "5B": Math.random(),
          //   "5C": Math.random(),
          //   "5D": Math.random(),
          //   "5E": Math.random(),
          //   "5F": Math.random(),
          //   "5G": Math.random(),
          //   "5H": Math.random(),
          //   "6A": Math.random(),
          //   "6B": Math.random(),
          //   "6C": Math.random(),
          //   "6D": Math.random(),
          //   "6E": Math.random(),
          //   "6F": Math.random(),
          //   "7A": Math.random(),
          //   "7B": Math.random(),
          //   "7C": Math.random(),
          //   "7D": Math.random(),
          //   "7E": Math.random(),
          //   "7F": Math.random(),
          //   "7G": Math.random(),
          //   "8A": Math.random(),
          //   "8B": Math.random(),
          //   "8C": Math.random(),
          //   "8D": Math.random(),
          //   "8E": Math.random(),
          //   "8F": Math.random(),
          //   "8G": Math.random(),
          //   "9A": Math.random(),
          //   "9B": Math.random(),
          //   "9C": Math.random(),
          //   "9D": Math.random(),
          //   "9E": Math.random(),
          //   "9F": Math.random(),
          //   "9G": Math.random(),
          // };
          /**
           * 맵 객체를 전달하여 여러개의 블록을 그리는 함수
           */
          createBlocks(
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
          createBlocks(
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
          createBlocks(
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
          createBlocks(
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
          createBlocks(
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
          createBlocks(
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
          createBlocks(
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
          createBlocks(
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
          createBlocks(
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
      <div id="cpvs">
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
  );
};

export default CPVS;
