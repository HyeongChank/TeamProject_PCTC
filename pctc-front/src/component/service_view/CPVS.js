/* Level 3 */
/* Congestion prediction and visualization service */
/* 혼잡도 예측 및 시각화 서비스 */
import { useEffect, useState } from 'react';
import './serviceview.css'
import Block from './component/Block';

const { kakao } = window;

const CPVS = ({ isLogin }) => {

  const [serviceViewOpacity, setServiceViewOpacity] = useState(0);

  const kakaoMap = <div id="map" style={{ width: '100%', height: '100%', opacity: serviceViewOpacity }}>
    <div id="area-1" style={{ opacity: serviceViewOpacity }} className='area-anim'></div>
    <div id="area-2" style={{ opacity: serviceViewOpacity }} className='area-anim'></div>
    <div id="area-3" style={{ opacity: serviceViewOpacity }} className='area-anim'></div>
  </div>

  let block = [
    ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I'],
    ['2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I'],
    // ['3A', '3B', '3C', '3D', '3E', '3F', '3G', '3H', '3I'],
    // ['4A', '4B', '4C', '4D', '4E', '4F', '4G', '4H', '4I'],
    // ['5A', '5B', '5C', '5D', '5E', '5F', '5G'],
    // ['6A', '6B', '6C', '6D', '6E', '6F', '6G'],
    // ['7A', '7B', '7C', '7D', '7E', '7F', '7G'],
    // ['8A', '8B', '8C', '8D', '8E', '8F', '8G'],
    // ['9A', '9B', '9C', '9D', '9E', '9F', '9G'],
  ]

  let X축 = 320;
  let Y축 = 410;

  block = block.map((column) => {
    return column.map((nameText) => {
      return {
        nameText: {
          "name": nameText,
          "congestion": Math.random(),
          "sizeWidth": 400,
          "sizeHeight": 70,
          "scale": 0.1,
          "locationX": `${X축}px`,
          "locationY": `${Y축}px`,
        }
      }
    })
  })

  block = block.map((column) => {
    Y축 = 410;
    X축 += (500 * 0.1);
    return column.map((blockData) => {
      Y축 -= 30;
      blockData.nameText.locationX = `${X축}px`;
      blockData.nameText.locationY = `${Y축}px`;
      return <Block key={blockData.nameText.name} blockData={blockData} />
    })
  })
  console.log("block:", block)


  useEffect(() => {
    if (isLogin) {
      setServiceViewOpacity(1)
      var container = document.getElementById('map');
      var options = {
        center: new kakao.maps.LatLng(35.106, 129.08),
        level: 4,
        draggable: false,
        disableDoubleClickZoom: true,
      };

      var map = new kakao.maps.Map(container, options);
    } else {
      setServiceViewOpacity(0)
    }
  }, [isLogin]);

  return (
    <div className='cpvs'>
      <div id="map" style={{ width: '100%', height: '100%', opacity: serviceViewOpacity }}>
        <article>
          {block}/
        </article>
      </div>
    </div>
  )
}

export default CPVS;