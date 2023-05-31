import { createShip } from "./createShip";

/**
 *
 * @param kakao 카카오 맵 오브젝트(window.kakao)
 * @param flag 블록들이 표시될 기준 위경도
 * @param blockSize 각 블록의 사이즈(단일)
 * @param repeat 몇개나 만들 것인가?
 * @returns 블록의 집합
 */
export function createShips(
  kakao: any,
  flag: [number, number][],
  map: any,
  completeWorking: number[]
) {
  const rectangles = [];
  const blockAddress = ["A","B","C","D","E","F","G","H","I","J",];

  for (let i = 0; i < flag.length; i++) {
    const ship = createShip(kakao, flag[i], map, completeWorking[i]);
    // ship.setMap(map);
    // flag = anything.nextPosition;
  }
}
