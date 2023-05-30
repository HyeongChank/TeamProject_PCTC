'use client'

export default function TitleMenu(props: any) {

  function onClick(menu: string) {

  }

  return (
    <>
      <button onClick={() => {onClick(props.name)}}>{props.name}</button>
      <style jsx>{`
      button, button:visited {
        display: inline-block;
        position: static;
        font-size: 1.2em;
        font-weight: bold;
        text-shadow: none;
        margin: 0 5px 0 5px;
        border: none;
        background: none;
        color: #282828;
      }
      
      button:hover {
        position: relative;
        bottom: 1px;
        right: 1px;
        text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.5);
      }
      
      button:active {
        position: relative;
        bottom: 0px;
        right: 0px;
        text-shadow: none;
      }
      `}</style>
    </>
  );
}