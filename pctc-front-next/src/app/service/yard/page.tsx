import YardStatus from "@/app/components/client/serviceview/YardStatus";
import { cookies } from "next/dist/client/components/headers";
import styles from "./styles.module.css";

export default async function BAS() {
  if (cookies().get("isLogin")?.value === "true") {
    return (
      <>
        <section className={styles.section}>
          <YardStatus apiKey={process.env.KAKAO_MAP_API_KEY} />
        </section>
      </>
    );
  } else {
    return <></>;
  }
}
