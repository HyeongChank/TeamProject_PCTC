"use client";

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import resourceTimelinePlugin from "@fullcalendar/resource-timeline";
import timeGridPlugin from "@fullcalendar/timegrid";
import timelinePlugin from "@fullcalendar/timeline";
import { useEffect, useRef } from "react";

export default function Calendar() {
  const calendarRef = useRef(null);

  useEffect(() => {
    const calendarEl = calendarRef.current;

    return () => {};
  }, []);

  return <div ref={calendarRef} />;
}
