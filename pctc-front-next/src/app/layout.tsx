import { Providers } from "@/redux/provider";
import { Gowun_Dodum } from "next/font/google";
import "./globals.css";
import TitleView from "./TitleView";

const gowun_dodum = Gowun_Dodum({ subsets: ["latin"], weight: "400" });

export const metadata = {
  title: "컨테이너 터미널 혼잡도 분석 예측 웹서비스",
  description:
    "항만의 컨테이너 터미널 내 혼잡도를 분석 및 예측하여 화물 업체 및 기사의 운송 효율을 높여주기 위한 웹서비스입니다.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className={gowun_dodum.className}>
        <Providers>
          <TitleView />
          {children}
        </Providers>
      </body>
    </html>
  );
}


