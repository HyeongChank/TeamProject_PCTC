import './block.css'

/**
 * 
 * @param {number} locationX
 * @param {number} locationY
 * @param {number} congestion
 * @param {number} sizeWidth
 * @param {number} sizeHeight
 * @param {number} scale
 * @returns 
 */
export default function Block({ blockData }) {

  console.log(blockData.nameText)

  const fontScale = `${(blockData.nameText.sizeHeight * blockData.nameText.scale) / 20}em`;

  let lampColor = "";

  if(blockData.nameText.congestion < 0.5){
    // 원활(그린)
    lampColor = "lamp-green";
  } else if (blockData.nameText.congestion < 0.9) {
    // 혼잡(오렌지)
    lampColor = "lamp-orange";
  } else {
    // 매우 혼잡(레드)
    lampColor = "lamp-red"
  }

  return (
    <span className={lampColor}
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        position: 'relative',
        top: blockData.nameText.locationY,
        left: blockData.nameText.locationX,
        width: blockData.nameText.sizeWidth * blockData.nameText.scale,
        height: blockData.nameText.sizeHeight * blockData.nameText.scale,
        border: 'solid 1px #282828',
        fontSize: fontScale,
        zIndex: 10
      }} >
        {blockData.nameText.name}
    </span>
  );
}