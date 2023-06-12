import { Gowun_Dodum } from "next/font/google";
import styles from "./styles.module.css";

const gowun_dodum = Gowun_Dodum({ subsets: ["latin"], weight: "400" });

export const metadata = {
  title: "Dashboard",
  description: "..",
};

export default function Layout({
  children,
  cpvs,
  chart1,
  chart2,
}: {
  children: React.ReactNode;
  cpvs: React.ReactNode;
  chart1: React.ReactNode;
  chart2: React.ReactNode;
}) {
  return (
    <main className={styles.dashboard}>
      {children}
      {cpvs}
      <section className={styles.section}>
        {chart1}
        {chart2}
      </section>
    </main>
  );
}
