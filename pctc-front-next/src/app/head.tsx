import Script from "next/script";

export default function head(){
  return (
    <><Script type='text/javascript' src='//dapi.kakao.com/v2/maps/sdk.js?appkey=0ed00b3cb3e60ff887b0375a881a9b12' /></>
  );
}