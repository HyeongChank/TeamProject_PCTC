"use client";

import { useEffect, useRef, useState } from "react";
import { createShips } from "./createShips";

declare global {
  interface Window {
    kakao: any;
  }
}

let rendering = 0;

export default function SWS() {
  const [apiKey, setApiKey] = useState("");

  const container = useRef(null);

  useEffect(() => {
    const fetchApiKey = async () => {
      if (process.env.NODE_ENV === "development") {
        const res = await fetch("http://localhost:3000/api/data/getkey", {
          headers: {
            "Content-Type": "application/json",
          },
          method: "POST",
          body: JSON.stringify({
            token: "ABCDEFGH", // 임시 하드코딩. 추후 back에서 받을것.
          }),
        });
        setApiKey(await res.text());
      } else if (process.env.NODE_ENV === "production") {
        setApiKey("");
      } else {
        console.log("환경 변수를 확인할 수 없습니다.");
      }
    };
    fetchApiKey();
  }, []);

  useEffect(() => {
    rendering++;
    console.log(rendering);
    if (apiKey !== "") {
      const script = document.createElement("script");
      script.src =
        "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + apiKey + "&autoload=false";
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
                standardPoint[0] + 0.001,
                standardPoint[1] - 0.006
              ),
              level: 4,
              draggable: false,
              disableDoubleClickZoom: true,
            };
            const map = new kakao.maps.Map(mapContainer, mapOption);
            map.addOverlayMapTypeId(kakao.maps.MapTypeId.TERRAIN);

            createShips(
              kakao,
              [
                [35.1086, 129.093], // 배 위치는 일단 하드코딩으로 해둠. 추후 Back에서 데이터 받기.
                [35.1078, 129.0934],
                [35.107, 129.093],
                [35.1062, 129.0931],
                [35.1053, 129.0932],
                [35.1045, 129.0933],
                [35.103, 129.0885],
                [35.103, 129.085],
                [35.103, 129.0815],
              ],
              map,
              [
                Math.round(Math.random() * 100), // 배마다 작업완료 수준 프로그레스바 하드코딩. 추후 데이터 보완.
                Math.round(Math.random() * 100),
                Math.round(Math.random() * 100),
                Math.round(Math.random() * 100),
                Math.round(Math.random() * 100),
                Math.round(Math.random() * 100),
                Math.round(Math.random() * 100),
                Math.round(Math.random() * 100),
                Math.round(Math.random() * 100),
              ]
            );
          });
        }
      };
    }
  }, [container, apiKey]);

  return (
    <>
      <div className="sws">
        <div id="container" ref={container} />
      </div>
      <style jsx>{`
        .sws {
          display: flex;
          z-index: 0;
        }
        #container {
          width: 80vw;
          height: 80vh;
          border: solid 1px #282828;
          border-radius: 10px;
          z-index: 0;
        }
      `}</style>
    </>
  );
}
