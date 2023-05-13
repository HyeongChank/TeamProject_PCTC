/** CTS: Container transport status (컨테이너 반출입현황) */

import CreateTable from "./CreateTable";
import IntroMenu from "./IntroMenu";

export default function CTS() {
  return (
    <>
      <IntroMenu menu='컨테이너터미널 반출입현황' />
      <CreateTable cols={13} />
    </>
  );
}