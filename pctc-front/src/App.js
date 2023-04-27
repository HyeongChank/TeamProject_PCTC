/* Level 0 */
import './App.css';

import FooterView from "./component/FooterView";
import Middle from "./component/Middle";
import ServiceView from "./component/ServiceView";
import TitleView from "./component/TitleView";

function App() {
  return (
    <>
      <TitleView />
      <Middle />
      <ServiceView />
      <FooterView />
    </>
  );
}

export default App;
