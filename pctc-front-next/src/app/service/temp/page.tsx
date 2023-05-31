// 쓰는 페이지 아님. 저장용.
"use client";

import React, { useEffect, useRef } from "react";
import "ol/ol.css";
import Map from "ol/Map";
import View from "ol/View";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { fromLonLat, transform } from "ol/proj";


export default function TempPage() {
  
  const mapRef = useRef(null);

  useEffect(() => {
    
    if (mapRef.current) {
      const map = new Map({
        target: mapRef.current,
        layers: [
          new TileLayer({
            source: new OSM(),
          }),
        ],
        view: new View({
          center: transform([129.0306, 35.0779], "EPSG:4326", "EPSG:3857"),
          zoom: 15,
          maxZoom: 19,
          minZoom: 10,
        }),
      });

      
    }
  }, []);


  return <div id="map" className="map-container" ref={mapRef} style={{width: "70vw", height:"70vh"}} />;
}
