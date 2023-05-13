/** BAS: Berth Assignment Status (선석배정현황) */

import CreateTable from "./CreateTable";
import IntroMenu from "./IntroMenu";

export default function BAS() {
  return (
    <>
      <IntroMenu menu='선박배정현황' />
      <CreateTable cols={13} />
    </>
  );
}