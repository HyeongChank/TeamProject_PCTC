import ChartTotalEmptyContainer from "@/app/components/client/serviceview/ChartTotalEmptyContainer";
import { cookies } from "next/dist/client/components/headers";
import styles from "./styles.module.css";

export default function CTS() {
  if (cookies().get("isLogin")?.value === "true") {
    return (
      <>
        <main className={styles.section}>
          <ChartTotalEmptyContainer
            title="선사별 공컨테이너 수"
            legend={["선사", "공컨테이너 수"]}
            data={[
              33, 81, 34, 171, 118, 2, 52, 338, 12, 35, 7, 12, 112, 73, 65, 42,
              354, 11, 7, 27, 13, 11, 30, 11, 44,
            ]}
            labels={[
              "CKL",
              "CMA",
              "COS",
              "DJS",
              "DYS",
              "GFL",
              "HAD",
              "HAS",
              "HHS",
              "HMM",
              "HSL",
              "HXD",
              "KMD",
              "NSL",
              "PCL",
              "POL",
              "SKR",
              "SML",
              "TCL",
              "TJM",
              "TMS",
              "TSL",
              "WSL",
              "YML",
              "ZIM",
            ]}
            width={50}
            height={40}
          />
        </main>
      </>
    );
  } else {
    return <></>;
  }
}
