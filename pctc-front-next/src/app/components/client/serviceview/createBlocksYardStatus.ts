import { createBlockYardStatus } from "./createBlockYardStatus";

/**
 *
 * @param kakao 카카오 맵 오브젝트(window.kakao)
 * @param flag 블록들이 표시될 기준 위경도
 * @param blockSize 각 블록의 사이즈(단일)
 * @param repeat 몇개나 만들 것인가?
 * @returns 블록의 집합
 */
export function createBlocksYardStatus(
  kakao: any,
  flag: any,
  blockSize: [number, number],
  repeat = 1,
  map: any,
  blockColumn: number, // 1A에서 1에 해당함.
  blockStatus: any // 추후 Input 방식 결정되면 타입 정의해야함.
) {
  const rectangles = [];
  const blockAddress = ["A","B","C","D","E","F","G","H","I","J","K",];
  for (let i = 0; i < repeat; i++) {
    const blockName = blockColumn + blockAddress[i];
    const anything = createBlockYardStatus(kakao, flag, blockSize, map, blockName, blockStatus[blockColumn + blockAddress[i]]);
    anything.polygon.setMap(map);
    flag = anything.nextPosition;
  }
}
