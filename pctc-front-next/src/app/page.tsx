import { cookies } from "next/dist/client/components/headers";
import { redirect } from "next/navigation";
import Intro from "./Intro";

export default function Home() {
  // if (true) {
  if (cookies().get("isLogin")?.value === "true") {
    redirect("/dashboard");
  } else {
    return (
      <main id="root-main">
        <Intro />
      </main>
    );
  }
}
