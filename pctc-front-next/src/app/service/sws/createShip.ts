import './ship.css';

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
  completeWorking: number
) {
  function createOverlay() {
    let overlay = new kakao.maps.CustomOverlay();
    let content = `
    <div class="ship-working">
      <progress class="ship-complete-working" value=${completeWorking} max="100"></progress>
      <div class="ship">
        <img src="/ship.svg"/>
      </div>
    </div>
    `;

    // 마커 위에 커스텀오버레이를 표시합니다
    // 마커를 중심으로 커스텀 오버레이를 표시하기위해 CSS를 이용해 위치를 설정했습니다
    overlay = new kakao.maps.CustomOverlay({
      content: content,
      map: map,
      position: new kakao.maps.LatLng(flag[0], flag[1]),
    });
    return overlay;
  }

  return createOverlay();
}
