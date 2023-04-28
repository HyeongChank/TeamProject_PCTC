/* Level 3 */
/* Congestion prediction and visualization service */
/* 혼잡도 예측 및 시각화 서비스 */
import { useState } from 'react';
import BarChart from './component/BarChart';
import './serviceview.css'
import { UserData } from './component/Data';


const CPVS = () => {
  
  const [userData, setUserData] = useState({
    labels: UserData.map((x) => x.year),
    datasets: [{
      label: "Users Gained",
      data: UserData.map((x) => x.userGain),
    },{
      label: "Users Gained2",
      data: UserData.map((x) => x.userLost),
    }]
  });

  return(
    <div className='cpvs'>
      <div style={{'fontSize': '2em', fontWeight:'bold', textAlign: 'center'}}>CPVS Area</div>
      <div style={{width: '700px', height:'700px'}}>
        <BarChart chartData={userData} />
      </div>
    </div>
  )
}

export default CPVS;