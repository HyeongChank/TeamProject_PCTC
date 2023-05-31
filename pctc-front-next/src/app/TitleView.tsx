/* server */

import Image from "next/image";
import Link from "next/link";
import Signin from "./components/client/signin/Signin";
import TitleMenu from "./TitleMenu";

const TitleView = () => {
  return (
    <div className="flex h-24 items-center">
      <div className="w-2/12 h-16 m-3 flex justify-center items-center">
        <Link href="/">
          <Image src="/logo.png" alt="logo" width={205} height={62} />
        </Link>
      </div>
      <div className="w-1/12"></div>
      <div className="w-7/12 h-16 flex items-center justify-between">
        <Link href="/service/sws">
          <TitleMenu name="본선작업현황" />
        </Link>
        <Link href="/service/yard">
          <TitleMenu name="야드작업현황" />
        </Link>
        <Link href="/service/empty">
          <TitleMenu name="공컨테이너 현황(신선대)" />
        </Link>
        <Link href="/service/shipinout">
          <TitleMenu name="선박입출항예정정보 " />
        </Link>
      </div>
      <div className="w-1/12"></div>
      <div className="w-1/12 h-16">
        <Signin />
      </div>
    </div>
  );
};

export default TitleView;
