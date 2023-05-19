"use client";

import { useEffect, useRef, useState } from "react";

declare global {
  interface Window {
    kakao: any;
  }
}

export default function SWS() {
  const [apiKey, setApiKey] = useState("");
  
  const container = useRef(null);
  (async function (){
    const res = await fetch('/api/data/getkey', {
      headers: {
        'Content-Type': 'application/json'
      },
      method: "POST",
      body: JSON.stringify({
        token: "회원 토큰",
      })
    })
    setApiKey(await res.text())
  })()

  
  


  useEffect(() => {
    if(apiKey !== ""){
      const script = document.createElement("script");
      script.src =
        "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + apiKey + "&autoload=false";
      document.head.appendChild(script);
  
      script.onload = () => {
        if (typeof window !== "undefined") {
          const { kakao } = window;
          kakao.maps.load(() => {
            const mapContainer = document.getElementById("container");
            const mapOption = {
              center: new kakao.maps.LatLng(35.106, 129.08),
              level: 4,
              draggable: false,
              disableDoubleClickZoom: true,
            };
            const map = new kakao.maps.Map(mapContainer, mapOption);
            map.addOverlayMapTypeId(kakao.maps.MapTypeId.TERRAIN);    
          });
        }
      };
      window.addEventListener('devtoolschange', event => {
       console.log("ddddddddd");
     });
    }
  }, [container, apiKey]);

  return (
    <>
      <div className="sws">
        <div id="container" ref={container} />
        {/* <Table tableTitle={"본선작업현황"} tableHead={["번호","터미널","선석","작업QC번호","모선항차","작업시작시간","작업완료시간","양하작업물량-작업량","양하작업물량-완료량","양하작업물량-잔여량","적하작업물량-작업량","적하작업물량-완료량","적하작업물량-잔여량","합계-작업량","합계-완료량","합계-잔여량"]} /> */}
      </div>
      <style jsx>{`
        #container {
          width: 70vw;
          height: 70vh;
          border: solid 1px #282828;
          border-radius: 10px;
        }
      `}</style>
    </>
  );
}
