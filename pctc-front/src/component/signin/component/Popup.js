import Modal from 'react-modal';

export default function Popup({ popupIsOpen, popupInfo, translater, buttonFunction }) {

  const ModalStyle = {
    overlay: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(255,255,255,0)',
      zIndex: 10,
    },
    content: {
      backgroundColor: 'white',
      top: '200px',
      left: '675px',
      right: '675px',
      bottom: '200px',
    }
  };

  function onClick(content, company) {
    buttonFunction(content, company)
  }

  let loopList = ['카카오', '네이버', '구글'];

  loopList = loopList.map((company) =>
    <button key={translater[company]} className={`submit_btn ${translater[company]}`} onClick={() => onClick(translater[popupInfo.content], translater[company])}>{company + popupInfo.action}</button>
  )

  return (
    <Modal style={ModalStyle} isOpen={popupIsOpen} >
      {popupInfo.content}
      {loopList}
    </Modal>
  );

}