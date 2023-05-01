import FooterView from "./FooterView";
import Middle from "./Middle";
import ServiceView from "./ServiceView";
import TitleView from "./TitleView";

const Home = (props) => {
  return (
    <>
      <TitleView isLogin={props.isLogin} setIsLogin={props.setIsLogin}/>
      <Middle />
      <ServiceView isLogin={props.isLogin} />
      <FooterView />
    </>
  )
}

export default Home;