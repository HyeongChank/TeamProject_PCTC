import FooterView from "./FooterView";
import ServiceView from "./ServiceView";

const Home = ({isLogin, setIsLogin}) => {
  return (
    <>
      <ServiceView isLogin={isLogin} />
      <FooterView />
    </>
  )
}

export default Home;