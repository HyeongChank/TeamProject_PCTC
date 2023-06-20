"use client";

import { CalendarApi } from "@fullcalendar/core";
import { formatIsoMonthStr } from "@fullcalendar/core/internal";
import FullCalendar from "@fullcalendar/react";
import resourceTimelinePlugin from "@fullcalendar/resource-timeline";
import { useEffect, useState } from "react";
import { format } from "date-fns";
import { AiOutlineHome } from "react-icons/ai";

export default function Calendar() {
  const events = [
    {
      resourceId: "1",
      title: "NSEP-9(P)",
      start: new Date("2023-06-20T03:10:00"),
      end: new Date("2023-06-20T22:30:00"),
    },
    {
      resourceId: "1",
      title: "NSEP-9(P)",
      start: new Date("2023-06-20T03:10:00"),
      end: new Date("2023-06-20T22:30:00"),
    },
    {
      resourceId: "1",
      title: "NSEP-9(P)",
      start: new Date("2023-06-20T03:10:00"),
      end: new Date("2023-06-20T22:30:00"),
    },
    {
      resourceId: "1",
      title: "NSEP-9(P)",
      start: new Date("2023-06-20T03:10:00"),
      end: new Date("2023-06-20T22:30:00"),
    },
    {
      resourceId: "2",
      title: "JXRN-23(S)",
      start: new Date("2023-06-20T06:00:00"),
      end: new Date("2023-06-21T07:30:00"),
    },
    {
      resourceId: "3",
      title: "PCMC-23(S)",
      start: new Date("2023-06-19T17:30:00"),
      end: new Date("2023-06-21T03:30:00"),
    },
    {
      resourceId: "4",
      title: "KSCM-25(P)",
      start: new Date("2023-06-19T23:00:00"),
      end: new Date("2023-06-23T00:00:00"),
    },
    {
      resourceId: "5",
      title: "HNVY-5(S)",
      start: new Date("2023-06-21T07:00:00"),
      end: new Date("2023-06-22T22:30:00"),
    },
    {
      resourceId: "6",
      title: "OLYM-4(S)",
      start: new Date("2023-06-20T06:00:00"),
      end: new Date("2023-06-22T03:30:00"),
    },
    {
      resourceId: "7",
      title: "DJCF-8(S)",
      start: new Date("2023-06-20T00:00:00"),
      end: new Date("2023-06-21T15:00:00"),
    },
    {
      resourceId: "8",
      title: "NSTP-9(P)",
      start: new Date("2023-06-19T23:00:00"),
      end: new Date("2023-06-22T17:30:00"),
    },
  ];

  const resources = [
    { id: "1", title: "1번 선석" },
    { id: "2", title: "2번 선석" },
    { id: "3", title: "3번 선석" },
    { id: "4", title: "4번 선석" },
    { id: "5", title: "5번 선석" },
    { id: "6", title: "6번 선석" },
    { id: "7", title: "7번 선석" },
    { id: "8", title: "8번 선석" },
  ];

  const [prevClassName, setPrevClassName] = useState("");
  const [homeClassName, setHomeClassName] = useState("");
  const [nextClassName, setNextClassName] = useState("");

  const [calendarApi, setCalendarApi] = useState<CalendarApi | null>(null);
  const [currentDate, setCurrentDate] = useState(
    format(new Date(), "yyyy년 MM월 dd일")
  );

  //event.clientY;

  useEffect(() => {
    if (calendarApi) {
      setCurrentDate(format(calendarApi.getDate(), "yyyy년 MM월 dd일"));
    }
  }, [calendarApi]);

  const handleToday = () => {
    if (calendarApi) {
      calendarApi.today();
      setCurrentDate(format(calendarApi.getDate(), "yyyy년 MM월 dd일"));
    }
  };

  const handlePrev = () => {
    if (calendarApi) {
      calendarApi.prev();
      setCurrentDate(format(calendarApi.getDate(), "yyyy년 MM월 dd일"));
    }
  };

  const handleNext = () => {
    if (calendarApi) {
      calendarApi.next();
      setCurrentDate(format(calendarApi.getDate(), "yyyy년 MM월 dd일"));
    }
  };

  return (
    <>
      <div>
        <h1>{currentDate}</h1>
        <article>
          <button
            className={homeClassName}
            onMouseOver={() => {
              setHomeClassName("feed-button-mouseover");
            }}
            onMouseLeave={() => {
              setHomeClassName("feed-button-mouseleave");
            }}
            onClick={handleToday}
          >
            <AiOutlineHome />
          </button>
          <button
            className={prevClassName}
            onMouseOver={() => {
              setPrevClassName("feed-button-mouseover");
            }}
            onMouseLeave={() => {
              setPrevClassName("feed-button-mouseleave");
            }}
            onClick={handlePrev}
          >
            &lt;
          </button>
          <button
            className={nextClassName}
            onMouseOver={() => {
              setNextClassName("feed-button-mouseover");
            }}
            onMouseLeave={() => {
              setNextClassName("feed-button-mouseleave");
            }}
            onClick={handleNext}
          >
            &gt;
          </button>
        </article>
        <FullCalendar
          plugins={[resourceTimelinePlugin]}
          initialView="resourceTimelineDay"
          events={events}
          resources={resources}
          height={events.length < 8 ? 410 : (events.length - 8) * 27 + 410} // events의 개수가 8개를 초과한 부분에 대해 기본 높이 410에서 27px씩 가산.
          headerToolbar={{}}
          slotMinWidth={10}
          slotLabelFormat={{ hour: "numeric", meridiem: false, hour12: false }}
          resourceAreaWidth="200px"
          ref={(calendarComponent) => {
            if (calendarComponent && calendarComponent.getApi) {
              setCalendarApi(calendarComponent.getApi());
            }
          }}
          eventMouseEnter={(info) => {
            console.log("Clicked on event: " + info.event.title);
          }}
        />
      </div>
      <style jsx>{`
        div {
          width: 80vw;
          margin: 4rem;
          padding: 4rem;
          text-align: center;
          background-color: white;
          border-radius: 5px;
          box-shadow: 3px 3px 2px 0px #14141480;
        }
        h1 {
          font-size: 2rem;
          font-weight: bold;
        }
        article {
          display: flex;
          flex-direction: row;
          justify-content: end;
          font-size: 1.7rem;
          font-weight: bold;
        }
        button {
          display: flex;
          justify-content: center;
          align-items: center;
          width: 2.5rem;
          height: 2.5rem;
          border-radius: 50%;
          margin-bottom: 0.5rem;
        }

        .feed-button-mouseover {
          animation-name: feed-button-anim-on;
          animation-duration: 0.5s;
          animation-fill-mode: forwards;
        }

        .feed-button-mouseleave {
          animation-name: feed-button-anim-off;
          animation-duration: 0.5s;
          animation-fill-mode: forwards;
        }

        @keyframes feed-button-anim-on {
          from {
            background-color: rgba(0, 0, 0, 0);
          }
          to {
            background-color: rgba(0, 0, 0, 0.2);
          }
        }

        @keyframes feed-button-anim-off {
          from {
            background-color: rgba(0, 0, 0, 0.2);
          }
          to {
            background-color: rgba(0, 0, 0, 0);
          }
        }
      `}</style>
    </>
  );
}
