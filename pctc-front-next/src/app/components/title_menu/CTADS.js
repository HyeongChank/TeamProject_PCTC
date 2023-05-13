/** CTADS: Container terminal arrival and departure status (컨테이너터미널 입출항 현황) */

import CreateTable from "./CreateTable";
import IntroMenu from "./IntroMenu";

export default function CTADS() {
  return (
    <>
      <IntroMenu menu='컨테이너터미널 입출항 현황' />
      <CreateTable cols={13} />
    </>
  );
}