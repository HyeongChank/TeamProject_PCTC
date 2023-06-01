import "./ship.css";
import { ShipDataValue } from "./makeShipDataValue";

interface Point {
  La: number;
  Ma: number;
}

type ConversionBlockSize = {
  NW: [number, number];
  SW: [number, number];
  SE: [number, number];
  NE: [number, number];
};

/**
 *
 * @param kakao 카카오 맵 오브젝트(window.kakao)
 * @param flag 블록들이 표시될 기준 위경도
 * @returns
 */
export function createShip(
  kakao: any,
  flag: [number, number],
  map: any,
  dataValue: ShipDataValue
) {
  let overlayShip = new kakao.maps.CustomOverlay();
  let overlayShip2 = new kakao.maps.CustomOverlay();

  const preUnloading = dataValue?.unloading.split("/");
  const preLoading = dataValue?.loading.split("/");
  const unloading = {
    scheduled: parseInt(preUnloading[0]),
    completed: parseInt(preUnloading[2]),
  };
  const loading = {
    scheduled: parseInt(preLoading[0]),
    completed: parseInt(preLoading[2]),
  };
  const completedWorking = unloading.completed + loading.completed;
  const scheduledWorking = unloading.scheduled + loading.scheduled;

  let content = `
  <div class="ship-working">
    <progress class="ship-complete-working" value=${completedWorking} max=${scheduledWorking}></progress>
    <div style="font-size: 0.6rem">${dataValue?.name}</div>
    <div class="ship">
      <img src="/ship.svg"/>
    </div>
  </div>
  `;

  /**
   * 선박 작업 완료율 표시 오버레이
   */
  function createOverlay() {
    // 마커를 중심으로 커스텀 오버레이를 표시하기위해 CSS를 이용해 위치를 설정했습니다
    overlayShip = new kakao.maps.CustomOverlay({
      content: content,
      map: map,
      zIndex: 1,
      position: new kakao.maps.LatLng(flag[0], flag[1]),
    });
    overlayShip.setMap(map);
    // return overlayShip;
  }

  function createOverlay2() {
    // 마커를 중심으로 커스텀 오버레이를 표시하기위해 CSS를 이용해 위치를 설정했습니다
    const preUnloading = dataValue.unloading.split("/");
    const preLoading = dataValue.loading.split("/");
    const unloading = {
      scheduled: preUnloading[0],
      completed: preUnloading[2],
    };
    const loading = {
      scheduled: preLoading[0],
      completed: preLoading[2],
    };

    overlayShip2 = new kakao.maps.CustomOverlay({
      content: `<div class="border rounded px-2 border-gray-800 bg-white flex flex-col justify-center items-center">
      <div style="width: 100%; text-align: center; border-bottom: solid 1px #000000; font-weight: bold">${dataValue.name}</div>
      <div style="width: 100%; text-align: center;">입항시간 | ${dataValue.arrival}</div> 
      <div style="width: 100%; text-align: center;">출항시간 | ${dataValue.departure}</div>
      <div class="temptemptemp" style="width: 100%; text-align: center;">양하 | <progress class="ship-unloading" value=${unloading.completed} max=${unloading.scheduled}></progress>${unloading.completed} / ${unloading.scheduled}</div>
      <div class="temptemptemp" style="width: 100%; text-align: center;">적하 | <progress class="ship-loading" value=${loading.completed} max=${loading.scheduled}></progress>${loading.completed} / ${loading.scheduled}</div>
                      </div>`,
      clickable: true,
      map: map,
      zIndex: 1,
      position: new kakao.maps.LatLng(flag[0] + 0.003, flag[1]),
    });

    overlayShip2.setMap(map);
  }

  function removeOverlay2() {
    overlayShip2.setMap(null);
  }

  var sw = new kakao.maps.LatLng(flag[0], flag[1] + 0.0025), // 사각형 영역의 남서쪽 좌표
    ne = new kakao.maps.LatLng(flag[0] + 0.0015, flag[1] - 0.0025); // 사각형 영역의 북동쪽 좌표

  // 사각형을 구성하는 영역정보를 생성합니다
  // 사각형을 생성할 때 영역정보는 LatLngBounds 객체로 넘겨줘야 합니다
  var rectangleBounds = new kakao.maps.LatLngBounds(sw, ne);

  // 지도에 표시할 사각형을 생성합니다
  var rectangle = new kakao.maps.Rectangle({
    bounds: rectangleBounds, // 그려질 사각형의 영역정보입니다
    strokeWeight: 4, // 선의 두께입니다
    strokeColor: "#FFFFFF", // 선의 색깔입니다
    strokeOpacity: 0, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
    strokeStyle: "solid", // 선의 스타일입니다
    fillColor: "#FFFFFF", // 채우기 색깔입니다
    fillOpacity: 0.01, // 채우기 불투명도 입니다
    zIndex: 10, // z 인덱스
  });

  // 지도에 사각형을 표시합니다
  rectangle.setMap(map);

  createOverlay();

  // 다각형에 마우스오버 이벤트를 등록합니다
  kakao.maps.event.addListener(rectangle, "mouseover", function () {
    createOverlay2();
  });

  kakao.maps.event.addListener(rectangle, "mouseout", function () {
    removeOverlay2();
  });

  // return createOverlay();
}
