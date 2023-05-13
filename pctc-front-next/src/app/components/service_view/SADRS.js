/* Level 3 */
/* Ship arrival date recommendation service */
/* 선박 입항일자 추천 서비스 */
import './serviceview.css'
import { useState } from 'react'


const SADRS = () => {

  const [temp, setTemp] = useState("");


  function test1() {
    fetch('http://10.125.121.222:8080/auth/signin', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors',
      body: JSON.stringify({
        username: "hello@world.com",
        password: "12345"
      })
    }).then(resp => resp.json())
    .then(result => {console.log(result)})
      .catch(error => {
        setTemp(error.toString())
      })
  }


  // function test2() {
  //   fetch('http://10.125.121.222:8080/test', {
  //     method: 'GET',
  //     mode: 'cors',
  //     headers: {
  //       'Content-Type': 'text/plain',
  //     }
  //   })
  //     .then(response => {
  //       alert(response)
  //     })
  // }




  return (
    <div className='sadrs'>
      <div style={{ 'fontSize': '2em', fontWeight: 'bold', textAlign: 'center' }}>SADRS Area</div>
      <div style={{ 'fontSize': '2em', fontWeight: 'bold', textAlign: 'center' }}>선박 입항일자 추천 서비스</div>
      <button onClick={test1}>ㅇㅇ</button>
      <div>{temp}</div>
      <form action='http://10.125.121.222:8080/auth/test' method='post'>
        <input type='text' name='username' />
        <input type='text' name='password' />
        <button type='submit'>ㅇㅇ</button>
      </form>
    </div>
  )
}

export default SADRS;