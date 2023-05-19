/* server */

import Image from "next/image";
import Link from "next/link";
import TitleMenu from "../client/TitleMenu";
import Signin from "../client/signin/Signin";

const TitleView = () => {

  return (
    <div className="flex h-24 items-center">
      <div className="w-2/12 h-16 m-3 flex justify-center items-center">
        <Link href='/'>
          <Image src='/logo.png' alt="logo" width={205} height={62} />

        </Link>
      </div>
      <div className="w-1/12"></div>
      <div className="w-7/12 h-16 flex items-center justify-between">
        <Link href='/service/bas'><TitleMenu name="선석배정현황" /></Link>
        <Link href='/service/sws'><TitleMenu name="본선작업현황" /></Link>
        <Link href='/service/cts'><TitleMenu name="컨테이너 반출입현황" /></Link>
        <Link href='/service/ctas'><TitleMenu name="컨테이너터미널 재박현황" /></Link>
        <Link href='/service/ctads'><TitleMenu name="컨테이너터미널 입출항현황" /></Link>
      </div>
      <div className="w-1/12"></div>
      <div className="w-1/12 h-16">
        <Signin />
      </div>
    </div>
  )
}

export default TitleView;