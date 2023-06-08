import YardStatus from "@/app/components/client/serviceview/YardStatus";

export default async function BAS() {

  return (
    <>
      <YardStatus apiKey={process.env.KAKAO_MAP_API_KEY} />
    </>
  );
}