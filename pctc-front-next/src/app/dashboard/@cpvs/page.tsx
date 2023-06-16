import CPVS from "@/app/components/client/serviceview/CPVS";

export default function CPVSPage() {
  return (
    <>
      <CPVS apiKey={process.env.KAKAO_MAP_API_KEY} />
    </>
  );
}
