/** SWS: Ship work status (본선작업현황) */

import CreateTable from "./CreateTable";
import IntroMenu from "./IntroMenu";

export default function SWS() {
  return (
    <>
      <IntroMenu menu='본선작업현황' />
      <CreateTable cols={13} />
    </>
  );
}