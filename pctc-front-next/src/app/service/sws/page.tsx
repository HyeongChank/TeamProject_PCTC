"use client";

import { useEffect, useRef, useState } from "react";
import { createShips } from "./createShips";
import { makeShipDataValue } from "./makeShipDataValue";
import { ShipDataValue } from "./makeShipDataValue";

declare global {
  interface Window {
    kakao: any;
  }
}

let rendering = 0;

export default function SWS() {
  const [apiKey, setApiKey] = useState("");
  const [dataValue, setDataValue] = useState<ShipDataValue[]>([]);

  const container = useRef(null);
  

  useEffect(() => {
    (async () => {
      // if (process.env.NODE_ENV === "development") {
      if (true) {
        const res = await fetch("http://10.125.121.207:3000/api/data/getkey", {
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
      const res = await fetch("http://10.125.121.222:8080/port");
      const data = await res.json();
      setDataValue(data as ShipDataValue[]);
      console.log("최초 렌더링!!!");
    })();

    setInterval(async () => {
      const res = await fetch("http://10.125.121.222:8080/port");
      const data = await res.json();
      setDataValue(data as ShipDataValue[]);
      console.log("재렌더링!!!");
    }, 10000);
  }, []);

  useEffect(() => {
    rendering++;
    console.log(rendering);

    setTimeout(() => {
      if (apiKey !== "") {
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
                map,
                dataValue
              );
            });
          }
        };
      }
    }, 1000);
  }, [container, apiKey, dataValue]);

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
