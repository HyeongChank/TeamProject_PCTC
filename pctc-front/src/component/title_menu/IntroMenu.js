/** 각 페이지의 소개탭 */

export default function IntroMenu({menu}){
  const IntroMenu_Style = {
    fontSize: '2em',
    fontWeight: 'bold',
    display: 'flex',
    justifyContent: 'center',
    marginTop: '10vh',
    marginBottom: '10vh',
  }
  
  return (
    <div style={IntroMenu_Style}>
      {menu}
    </div>
  );
}