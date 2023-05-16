import CPVS from "./components/client/serviceview/CPVS";

export default function Home() {
  return (
        <main>
          <CPVS apiKey={process.env.KAKAO_MAP_API_KEY ?? ""} />
        </main>
  )
}
