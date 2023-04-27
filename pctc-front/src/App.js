/* Level 0 */
import './App.css';

import FooterView from "./component/FooterView";
import Middle from "./component/Middle";
import ServiceView from "./component/ServiceView";
import TitleView from "./component/TitleView";
import Apps from './Apps';

function App() {
  return (
    <>
      <TitleView />
      <Middle />
      <ServiceView />
      <FooterView />
      {/* <Apps /> */}
    </>
  );
}

export default App;
