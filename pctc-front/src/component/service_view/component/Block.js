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
export default function Block({ locationX, locationY, congestion, sizeWidth, sizeHeight, scale }) {

  const fontScale = `${(sizeWidth * sizeHeight * scale) / 3000}em`;

  let lampColor = "";

  if(congestion < 0.5){
    // 원활(그린)
    lampColor = "lamp-green";
  } else if (congestion < 0.9) {
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
        top: locationY,
        left: locationX,
        width: sizeWidth * scale,
        height: sizeHeight * scale,
        border: 'solid 1px #282828',
        fontSize: fontScale,
        zIndex: 10
      }} >
        1A
    </span>
  );
}