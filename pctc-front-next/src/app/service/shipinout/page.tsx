import Calendar from "@/app/components/client/calendar/Calendar";
import styles from './styles.module.css';

export default function ShipInOut() {
  return (
    <>
      <section className={styles.section}>
        <Calendar />
      </section>
    </>
  );
}
