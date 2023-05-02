import './componentstyle.css'

export default function TitleMenu({ name }) {

  function onClick(menu) {

  }

  return (
    <button onClick={() => {onClick(name)}} className='titleMenu'>{name}</button>
  );
}