import { Point, ConversionBlockSize } from "./createBlock";

/**
 *
 * @param kakao 카카오 맵 오브젝트(window.kakao)
 * @param flag 블록들이 표시될 기준 위경도
 * @returns
 */
export function createBlockYardStatus(
  kakao: any,
  flag: {
    La: number;
    Ma: number;
  },
  blockSize: [number, number],
  map: any,
  blockName: string,
  blockStatus: number[]
) {
  const blockSizeConv = conversionMeterTo(blockSize);
  const gapCol = meterTo(-67); // 블럭 사이 간격(미터)
  const gapRow = meterTo(100); // 블럭 사이 간격(미터)
  let overlay = new kakao.maps.CustomOverlay();

  let polygonPath = [
    { Ma: flag.Ma + blockSizeConv.NW[0], La: flag.La + blockSizeConv.NW[1] },
    { Ma: flag.Ma + blockSizeConv.SW[0], La: flag.La + blockSizeConv.SW[1] },
    { Ma: flag.Ma + blockSizeConv.SE[0], La: flag.La + blockSizeConv.SE[1] },
    { Ma: flag.Ma + blockSizeConv.NE[0], La: flag.La + blockSizeConv.NE[1] },
  ];

  // let polygonPathRoteted = rotateRectangle(polygonPath, -5);
  let polygonPathRoteted = rotateRectangle(polygonPath, -94);
  let polygonPath2 = polygonPathRoteted.map((onePoint) => {
    return new kakao.maps.LatLng(onePoint.Ma, onePoint.La);
  });

  // 지도에 표시할 다각형을 생성합니다
  let polygon = new kakao.maps.Polygon({
    path: polygonPath2, // 그려질 다각형의 좌표 배열입니다
    strokeWeight: 1, // 선의 두께입니다
    strokeColor: "#000000", // 선의 색깔입니다
    strokeOpacity: 0, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
    strokeStyle: "solid", // 선의 스타일입니다
    fillColor: "#000000", // 채우기 색깔입니다
    fillOpacity: 0.5, // 채우기 불투명도 입니다
  });
  
  function createOverlay() {
    const center = {
      La: (polygonPathRoteted[0].La + polygonPathRoteted[2].La) / 2,
      Ma: (polygonPathRoteted[0].Ma + polygonPathRoteted[2].Ma) / 2 + 0.002,
    };
    let content = `<div class="border rounded px-2 border-gray-800 bg-white flex flex-col justify-center items-center">
    <div style="width: 100%; text-align: center; border-bottom: solid 1px #000000; font-weight: bold">${blockName}</div>
    <div style="width: 12vw; display: flex; flex-direction: row; justify-content: space-evenly;"><span style="display: inline-flex; width: 5vw; justify-content: center;">현재</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[0]
    }</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[1]
    }</span></div>
    <div style="width: 12vw; display: flex; flex-direction: row; justify-content: space-evenly;"><span style="display: inline-flex; width: 5vw; justify-content: center;">1시간 후</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[2]
    }</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[3]
    }</span></div>
    <div style="width: 12vw; display: flex; flex-direction: row; justify-content: space-evenly;"><span style="display: inline-flex; width: 5vw; justify-content: center;">2시간 후</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[4]
    }</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[5]
    }</span></div>
    <div style="width: 12vw; display: flex; flex-direction: row; justify-content: space-evenly;"><span style="display: inline-flex; width: 5vw; justify-content: center;">3시간 후</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[6]
    }</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[7]
    }</span></div>
    <div style="width: 12vw; display: flex; flex-direction: row; justify-content: space-evenly;"><span style="display: inline-flex; width: 5vw; justify-content: center;">4시간 후</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[8]
    }</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[9]
    }</span></div>
    <div style="width: 12vw; display: flex; flex-direction: row; justify-content: space-evenly;"><span style="display: inline-flex; width: 5vw; justify-content: center;">5시간 후</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[10]
    }</span><span style="border-left: 1px #282828 solid"> </span><span>${
      blockStatus[11]
    }</span></div>
                    </div>`;

    // 마커를 중심으로 커스텀 오버레이를 표시하기위해 CSS를 이용해 위치를 설정했습니다
    overlay = new kakao.maps.CustomOverlay({
      content: content,
      map: map,
      position: new kakao.maps.LatLng(center.Ma, center.La),
    });
    overlay.setMap(map);
  }

  // 커스텀 오버레이를 닫기 위해 호출되는 함수입니다
  function closeOverlay() {
    overlay.setMap(null);
  }

  // 다각형에 마우스오버 이벤트가 발생했을 때 변경할 채우기 옵션입니다
  let mouseoverOption = {
    fillColor: "#000", // 채우기 색깔입니다
    fillOpacity: 1, // 채우기 불투명도 입니다
  };

  // 다각형에 마우스아웃 이벤트가 발생했을 때 변경할 채우기 옵션입니다
  let mouseoutOption = {
    fillColor: "#000000", // 채우기 색깔입니다
    fillOpacity: 0.5, // 채우기 불투명도 입니다
  };

  // 다각형에 마우스오버 이벤트를 등록합니다
  kakao.maps.event.addListener(polygon, "mouseover", function () {
    // 다각형의 채우기 옵션을 변경합니다
    polygon.setOptions(mouseoverOption);
    createOverlay(); // 오버레이 그리기
  });

  kakao.maps.event.addListener(polygon, "mouseout", function () {
    // 다각형의 채우기 옵션을 변경합니다
    closeOverlay();
    overlay.setMap(null);
    polygon.setOptions(mouseoutOption);
  });

  return {
    polygon,
    nextPosition: new kakao.maps.LatLng(
      flag.Ma + blockSizeConv.NE[0] + gapCol,
      flag.La + blockSizeConv.NE[1] + gapRow
    ),
  };
}

/**
 * @param blockSize [가로길이, 세로길이] 블록사이즈 미터법으로 인풋 받음
 * @returns 가로세로 사이즈를 위경도 4개 포인트로 리턴
 */
function conversionMeterTo(blockSize: [number, number]) {
  let convertingBlockSize: ConversionBlockSize = {
    NW: [0, 0],
    SW: [0, meterTo(blockSize[1])],
    SE: [meterTo(blockSize[0]), meterTo(blockSize[1])],
    NE: [meterTo(blockSize[0]), 0],
  };

  return convertingBlockSize;
}

/**
 *
 * @param x 미터값
 * @returns 위경도 십진법으로 환산
 */
export function meterTo(x: number) {
  return x / 133333;
}

// 회전 계산된 좌표

function rotatePoint(center: Point, point: Point, angle: number): Point {
  const radians = (Math.PI / 180.0) * angle;
  const cos = Math.cos(radians);
  const sin = Math.sin(radians);

  const nx =
    cos * (point.La - center.La) + sin * (point.Ma - center.Ma) + center.La;

  const ny =
    cos * (point.Ma - center.Ma) - sin * (point.La - center.La) + center.Ma;

  return { La: nx, Ma: ny };
}

function rotateRectangle(rectangle: Point[], angle: number): Point[] {
  const center = {
    La: (rectangle[0].La + rectangle[2].La) / 2,
    Ma: (rectangle[0].Ma + rectangle[2].Ma) / 2,
  };

  return rectangle.map((point) => rotatePoint(center, point, angle));
}

/**
 *
 * @param blockStatus 블록의 적재율(0 - 1)
 * @returns 적재율의 수준에 따라 매우 혼잡, 혼잡, 보통, 원활 표시. 수준은 임의로 정했음.
 */
function blockStatusToString(blockStatus: number) {
  if (blockStatus < 200) {
    return { status: "원활", color: "#00BB00" };
  } else if (blockStatus < 300) {
    return { status: "보통", color: "#DDDD00" };
  } else if (blockStatus < 450) {
    return { status: "혼잡", color: "#FF8800" };
  } else {
    return { status: "매우 혼잡", color: "#CC0000" };
  }
}
