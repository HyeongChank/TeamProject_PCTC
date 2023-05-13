/** CTAS: Container Terminal Accommodation Status (컨테이너터미널 재박현황) */

import CreateTable from "./CreateTable";
import IntroMenu from "./IntroMenu";

export default function CTAS() {
  return (
    <>
      <IntroMenu menu='컨테이너터미널 재박현황' />
      <CreateTable cols={13} />
    </>
  );
}