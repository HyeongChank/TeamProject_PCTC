"use client";

export default function Intro() {
  return (
    <>
      <section>
        
      </section>
      <style jsx>{`
        section {
          width: 100vw;
          height: 882px;
          display: flex;
          justify-content: center;
          align-items: center;
          
          font-size: 2rem;
          background-image: url("/bgimage.jpg");
          background-size: cover;
          background-position: center;
          background-repeat: no-repeat;
        }
        section::after {
          content: "";
          position: absolute;
          top: 96px;
          left: 0px;
          width: 100vw;
          height: 100px;
          background: linear-gradient(to bottom, #FFFFFF, #FFFFFF00);
        }
      `}</style>
    </>
  );
}
