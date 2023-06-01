import { createShip } from "./createShip";
import { ShipDataValue } from "./makeShipDataValue";

const flag = [
  [
    [35.1086, 129.093],
    [35.1078, 129.0934],
  ],
  [
    [35.107, 129.093],
    [35.1062, 129.0931],
  ],
  [
    [35.1053, 129.0932],
    [35.1045, 129.0933],
  ],
  [
    [35.1037, 129.0934],
    [35.1029, 129.0935],
  ],
  [
    [35.1021, 129.0936],
    [35.1013, 129.0937],
  ],
  [
    [35.103, 129.0885],
    [35.103, 129.0865],
  ],
  [
    [35.103, 129.0835],
    [35.103, 129.0815],
  ],
  [
    [35.103, 129.0785],
    [35.103, 129.0765],
  ],
];

/**
 *
 * @param kakao 카카오 맵 오브젝트(window.kakao)
 * @param flag 블록들이 표시될 기준 위경도
 * @param blockSize 각 블록의 사이즈(단일)
 * @param repeat 몇개나 만들 것인가?
 * @returns 블록의 집합
 */
export function createShips(kakao: any, map: any, dataValue: ShipDataValue[]) {
  const rectangles = [];
  const blockAddress = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"];
  let prePortNo = "";
  let portDuple = 0;

  for (let i = 0; i < dataValue.length; i++) {
    if (prePortNo === dataValue[i].portorder) {
      portDuple++;
    } else {
      portDuple = 0;
    }
    prePortNo = dataValue[i].portorder;
    const ship = createShip(
      kakao,
      flag[parseInt(dataValue[i].portorder)][portDuple] as [number, number],
      map,
      dataValue[i]
    );
    // ship.setMap(map);
    // flag = anything.nextPosition;
  }
}
